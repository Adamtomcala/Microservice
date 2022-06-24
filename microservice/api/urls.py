from django.urls import path
from . import views

urlpatterns = [
    path('display_post', views.display_post, name="display"),
    path('display_user_post', views.display_user_posts, name="display_user_post"),
    path('create_post', views.create_post, name="create"),
    path('delete_post/<int:post_id>', views.delete_post, name="delete"),
    path('update_post_body/<int:post_id>', views.update_post_body, name="update_body"),
    path('update_post_title/<int:post_id>', views.update_post_title, name="update_title"),
]
