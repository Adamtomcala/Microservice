from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import Post
from .serializers import PostSerializer
import django.core.exceptions
import requests

URL = "https://jsonplaceholder.typicode.com"


# This function renders main page.
def main_page(request):
    if request.method == 'GET':
        user_id_form = UserIDForm()
        post_id_form = PostIDForm()

        context = {
            'user_id_form': user_id_form,
            'post_id_form': post_id_form
        }

        return render(request, 'app/base.html', context, status=200)


# This function returns create post page or creating new post. Depends on type of request.
@csrf_exempt
def create_post(request):
    # Creating a new post.
    if request.method == 'POST':
        # Checking if request contains parameter
        if 'user_id' not in request.POST:
            return render(request, 'app/error_page.html', {'error': 'Missing parameter'}, status=422)

        user_id = request.POST['user_id']

        # Checking format of parameter
        if user_id.isnumeric():
            response = requests.get(URL + "/users/" + user_id)
            data = response.json()

            # User does not exist
            if len(data) == 0:
                return render(request, 'app/error_page.html', {'error': 'User does not exist.'}, status=404)

            # Creating a new post
            new_post = Post.objects.create(user_id=user_id, title=request.POST['title'],
                                           description=request.POST['description'])
            new_post.save()

            ctx = {
                'data': PostSerializer(new_post).data,
                'message': 'This post was created.'
            }

            return render(request, 'app/info_page.html', ctx, status=200)
        else:
            return render(request, 'app/error_page.html', {'error': 'Bad format of user ID.'}, status=400)

    # Render create post page
    elif request.method == 'GET':
        form = PostForm()
        return render(request, 'app/create.html', {'form': form}, status=200)


# Function render page with one specific post or error page.
def get_post(request):
    if request.method == 'GET':
        # Checking if request contains parameter
        if 'post_id' in request.GET:
            # Checking if request contains parameter
            if request.GET.get('post_id').isnumeric():

                # Find post in DB
                try:
                    post = Post.objects.get(id=request.GET.get('post_id'))
                # Find post in Third Party API
                except django.core.exceptions.ObjectDoesNotExist as e:
                    url_post = requests.get(URL + '/posts/' + request.GET.get('post_id')).json()

                    # Wanted post does not exist
                    if len(url_post) == 0:
                        return render(request, 'app/error_page.html', {'error': 'Post does not exist.'}, status=404)

                    post = Post.objects.create(id=url_post['id'], user_id=url_post['userId'],
                                               title=url_post['title'], description=url_post['body'])
                    post.save()

                serializer = PostSerializer(post).data

                ctx = {
                    'posts': [serializer],
                }

                return render(request, 'app/display.html', ctx, status=200)

            # Wrong format of id (post id)
            else:
                return render(request, 'app/error_page.html', {'error': 'Bad format of post ID.'}, status=400)

        # Missing parameter
        else:
            return render(request, 'app/error_page.html', {'error': 'Missing parameter.'}, status=422)


# Function renders all posts of one user or error message.
def get_user_posts(request):
    if request.method == 'GET':

        if 'user_id' in request.GET:
            if request.GET.get('user_id').isnumeric():

                # Filter all posts of one user
                posts = Post.objects.filter(user_id=request.GET.get('user_id'))

                # This user does not upload any post
                if len(posts) == 0:
                    return render(request, 'app/error_page.html', {'error': 'User does not have any posts.'}, status=404)

                serialized_posts = []
                for post in posts:
                    serialized_posts.append(PostSerializer(post).data)

                ctx = {
                    'posts': serialized_posts,
                }

                return render(request, 'app/display.html', ctx, status=200)

            # Wrong format of user_id
            else:
                return render(request, 'app/error_page.html', {'error': 'Bad format of user ID.'}, status=400)

        # Missing parameter
        else:
            return render(request, 'app/error_page.html', {'error': 'Missing parameter.'}, status=422)


# This function renders delete post page.
def delete_post_page(request):
    if request.method == 'GET':
        post_id_form = PostIDForm()

        return render(request, 'app/delete.html', {'post_id_form': post_id_form})


# This function deletes post if exists or error page.
@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        try:
            put = QueryDict(request.body)
            post = Post.objects.get(id=put.get('post_id'))
        except django.core.exceptions.ObjectDoesNotExist:
            return render(request, 'app/error_page.html', {'error': 'Post with given ID does not exist.'}, status=404)

        ctx = {
            'data': PostSerializer(post).data,
            'message': 'This post was deleted.'
        }

        post.delete()

        return render(request, 'app/info_page.html', ctx, status=200)


# This function renders update post page.
def update_post_page(request, flag):
    if request.method == 'GET':
        # Render page with fields for title and body update
        if flag == 1:
            try:
                post = Post.objects.get(id=request.GET.get('post_id'))
            except django.core.exceptions.ObjectDoesNotExist:
                return render(request, 'app/error_page.html', {'error': 'Post does not exist.'}, status=404)

            context = {
                'body_form': BodyForm(),
                'title_form': TitleForm(),
                'flag': flag,
                'body': post.description,
                'title': post.title,
                'post_id': request.GET.get('post_id')
            }

            return render(request, 'app/update.html', context, status=200)
        # Render page with form for post id
        elif flag == 0:
            context = {
                'post_form': PostIDForm(),
                'flag': flag
            }
            return render(request, 'app/update.html', context, status=200)
        else:
            return render(request, 'app/error_page.html', {'error': 'Invalid argument.'}, status=400)


# This function updates post body and render results or error page.
@csrf_exempt
def update_post_body(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except django.core.exceptions.ObjectDoesNotExist:
            return render(request, 'app/error_page', {'error': 'Post does not exist.'}, status=404)

        if request.method == 'POST':
            if 'body' in request.POST:
                post.description = request.POST['body']
            else:
                return render(request, 'app/error_page', {'error': 'No parameter.'}, status=422)

            post.save()

            ctx = {
                'data': PostSerializer(post).data,
                'message': 'This post was updated.'
            }

            return render(request, 'app/info_page.html', ctx, status=200)


@csrf_exempt
def update_post_title(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except django.core.exceptions.ObjectDoesNotExist:
            return render(request, 'app/error_page', {'error': 'Post does not exist.'})

        if request.method == 'POST':
            if 'title' in request.POST:
                post.title = request.POST['title']
            else:
                return render(request, 'app/error_page', {'error': 'No parameter.'})

            post.save()

            ctx = {
                'data': PostSerializer(post).data,
                'message': 'This post was updated.'
            }

            return render(request, 'app/info_page.html', ctx)
