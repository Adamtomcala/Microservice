from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name="home"),
    path('create_post', views.create_post, name="create"),
    path('get_post', views.get_post, name="display_post"),
    path('get_user_posts', views.get_user_posts, name="display_user_posts"),
    path('delete_page', views.delete_post_page, name="delete_page"),
    path('delete_post', views.delete_post, name="delete"),
    path('update_page/<int:flag>', views.update_post_page, name="update_page"),
    path('update_post_body/<int:post_id>', views.update_post_body, name="update_post_body"),
    path('update_post_title/<int:post_id>', views.update_post_title, name="update_post_title"),
]
