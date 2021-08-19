from django.contrib.auth.models import User
from django.urls import path
from .views import (
    PostViewSet,
    CommentViewSet,
    UserDataViewSet,
)


urlpatterns = [
    path("posts/", PostViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        })),
    path("posts/<pk>", PostViewSet.as_view({
            'get' : 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy',
    })),
    path("posts/<pk>/like/", PostViewSet.as_view({
            'post' : 'like',
    })),
    path("posts/<pk>/bookmark/", PostViewSet.as_view({
            'post' : 'bookmark',
    })),
    path("posts/my_bookmarks/", PostViewSet.as_view({
            'get' : 'my_bookmarks',
    })),
    path("posts/hot/", PostViewSet.as_view({
            'get' : 'get_hot_posts',
    })),


    path("comments/", CommentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        })),
    path("comments/<pk>", CommentViewSet.as_view(
        {
            'get' : 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy'
        })),
    path("comments/<pk>/like/", CommentViewSet.as_view({
            'post' : 'like',
    })),
    path("comments/<pk>/bookmark/", CommentViewSet.as_view({
            'post' : 'bookmark',
    })),
    path("comments/my_bookmarks/", CommentViewSet.as_view({
            'get' : 'my_bookmarks',
    })),


    path("profile_photo/", UserDataViewSet.as_view(
        {
            'post': 'avatar_upload',
        })),
    path("user_data/", UserDataViewSet.as_view(
        {
            'put': 'data_update',
        })),
    path("activate/<uid>/<token>/", UserDataViewSet.as_view({
            'get' : 'activate',
    })),
    path("my_subscriptions/", UserDataViewSet.as_view(
        {
            'get': 'get_subscriptions',
    })),
    path("subscribe/<uname>", UserDataViewSet.as_view(
        {
            'post': 'subscribe',
    })),

]