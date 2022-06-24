import json
from django.views.decorators.csrf import csrf_exempt
from django.template.backends import django
import django.core.exceptions
from rest_framework.decorators import api_view

from .models import PostApi
from .serializers import PostApiSerializer
import requests
from django.http import JsonResponse, QueryDict

URL = "https://jsonplaceholder.typicode.com"


# Function returns one post or error message
def display_post(request):
    if request.method == 'GET':
        # Checking if request contains parameter
        if 'post_id' not in request.GET:
            return JsonResponse({'error': 'Missing parameter.'}, json_dumps_params={'indent': 3}, status=422)

        # Checking format of parameter
        if request.GET.get('post_id').isnumeric():
            # Find post in DB
            try:
                post = PostApi.objects.get(id=request.GET.get('post_id'))
            # Find post in Third Party API
            except django.core.exceptions.ObjectDoesNotExist as e:
                url_post = requests.get(URL + '/posts/' + request.GET.get('post_id')).json()
                # Wanted post does not exist
                if len(url_post) == 0:
                    return JsonResponse({'error': 'Post does not exists'}, json_dumps_params={'indent': 3},
                                        status=404)

                post = PostApi.objects.create(id=url_post['id'], user_id=url_post['userId'],
                                              title=url_post['title'], description=url_post['body'])
                post.save()

            serializer = PostApiSerializer(post).data

            return JsonResponse(serializer, json_dumps_params={'indent': 3}, status=200)

        # Wrong format of id (post id)
        else:
            return JsonResponse({'error': 'Bad format of post ID.'}, json_dumps_params={'indent': 3}, status=400)


# Function returns all posts of one user or error message
def display_user_posts(request):
    if request.method == 'GET':
        # Checking if request contains parameter
        if 'user_id' not in request.GET:
            return JsonResponse({'error': 'Missing parameter.'}, json_dumps_params={'indent': 3}, status=422)

        # Checking format of parameter
        if request.GET.get('user_id').isnumeric():

            # Filter all posts of one user
            posts = PostApi.objects.filter(user_id=request.GET.get('user_id'))

            # This user does not upload any post
            if len(posts) == 0:
                return JsonResponse({'error': 'User does not have any posts.'}, json_dumps_params={'indent': 3},
                                    status=404)

            serialized_posts = []
            for post in posts:
                serialized_posts.append(PostApiSerializer(post).data)

            return JsonResponse({'post': serialized_posts}, json_dumps_params={'indent': 3}, status=200)

        # Wrong format of user_id
        else:
            return JsonResponse({'error': 'Bad format of user ID.'}, json_dumps_params={'indent': 3}, status=400)


# Function creates a new post
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        # Checking if request contains parameters
        if 'user_id' not in request.POST or 'title' not in request.POST or 'description' not in request.POST:
            return JsonResponse({'error': 'Missing parameter.'}, json_dumps_params={'indent': 3}, status=422)

        user_id = request.POST['user_id']

        # Checking format of parameter
        if user_id.isnumeric():
            response = requests.get(URL + "/users/" + user_id)
            data = response.json()

            # User does not exist
            if len(data) == 0:
                return JsonResponse({'error': 'User does not exist.'}, json_dumps_params={'indent': 3}, status=404)

            # Creating a new post
            new_post = PostApi.objects.create(user_id=user_id, title=request.POST['title'],
                                           description=request.POST['description'])
            new_post.save()

            serializer = PostApiSerializer(new_post).data
            author = requests.get(URL + '/users/' + str(serializer['user_id'])).json()
            serializer['user_id'] = author['name']

            return JsonResponse(serializer, json_dumps_params={'indent': 3}, status=200)
        else:
            return JsonResponse({'error': 'Bad format of user ID.'}, json_dumps_params={'indent': 3}, status=400)


# Function deletes a post
@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'DELETE':
        try:
            post = PostApi.objects.get(id=post_id)
        except django.core.exceptions.ObjectDoesNotExist:
            return JsonResponse({'error': 'Post does not exists'}, json_dumps_params={'indent': 3}, status=404)

        serializer = PostApiSerializer(post).data
        post.delete()

        return JsonResponse(serializer, json_dumps_params={'indent': 3}, status=200)


# Function updates a title of post
@api_view(['PUT'])
@csrf_exempt
def update_post_title(request, post_id):
    if request.method == 'PUT':
        # Checking if request contains parameter
        if len(request.data) == 0:
            return JsonResponse({'error': 'Missing parameter.'}, json_dumps_params={'indent': 3}, status=422)

        body = request.data.dict()

        if 'title' not in body:
            return JsonResponse({'error': 'Invalid parameter.'}, json_dumps_params={'indent': 3}, status=404)

        try:
            post = PostApi.objects.get(id=post_id)
        except django.core.exceptions.ObjectDoesNotExist:
            return JsonResponse({'error': 'Post does not exists'}, json_dumps_params={'indent': 3}, status=404)

        post.title = body['title']

        post.save()

        return JsonResponse(PostApiSerializer(post).data, json_dumps_params={'indent': 3}, status=200)


# Function updates a body of post
@api_view(['PUT'])
@csrf_exempt
def update_post_body(request, post_id):
    if request.method == 'PUT':
        # Checking if request contains parameter
        if len(request.data) == 0:
            return JsonResponse({'error': 'Missing parameter.'}, json_dumps_params={'indent': 3}, status=422)

        body = request.data.dict()

        if 'body' not in body:
            return JsonResponse({'error': 'Invalid parameter.'}, json_dumps_params={'indent': 3}, status=404)

        try:
            post = PostApi.objects.get(id=post_id)
        except django.core.exceptions.ObjectDoesNotExist:
            return JsonResponse({'error': 'Post does not exists'}, json_dumps_params={'indent': 3}, status=404)

        post.description = body['body']

        post.save()

        return JsonResponse(PostApiSerializer(post).data, json_dumps_params={'indent': 3}, status=200)
