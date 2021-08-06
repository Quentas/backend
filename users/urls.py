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

    path("profile_photo/", UserDataViewSet.as_view(
        {
            'post': 'create',
        })),
    path("user_bio/", UserDataViewSet.as_view(
        {
            'put': 'partial_update',
        })),
    path("activate/<uid>/<token>/", UserDataViewSet.as_view({
            'get' : 'get',
    })),

]