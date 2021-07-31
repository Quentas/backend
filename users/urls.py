from django.contrib.auth.models import User
from django.urls import path
from .views import (
    PostViewSet,
    CommentViewSet,
    UploadUserPhotoViewSet,
    ActivateUser,
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


    path("comments/", CommentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        })),
    path("comments/<pk>", CommentViewSet.as_view(
        {
            'put': 'partial_update',
            'delete': 'destroy'
        })),
    path("comments/<pk>/like/", CommentViewSet.as_view({
            'post' : 'like',
    })),


    path("profile_photo/", UploadUserPhotoViewSet.as_view(
        {
            'post': 'create',
        })),
    path("activate/<uid>/<token>/", ActivateUser.as_view()),

]