from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.PostListView.as_view({'get': 'list'})),
    path("posts/user_id=<int:pk>", views.PostListView.as_view({'get': 'retrieve_user_id'})),
    path("posts/username=<str:username>", views.PostListView.as_view({'get': 'retrieve_username'})),
    path("posts/post_id=<int:pk>", views.PostListView.as_view({'get': 'retrieve_post'})),
]