from django.contrib.auth.models import User
from django.urls import path
from .views import (
    PostViewSet,
    CommentViewSet,
    UploadUserPhotoViewSet,
    ActivateUser,
    UsersMe,
    PostLikeViewSet,
)

urlpatterns = [
    path("posts/", PostViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'partial_update',
            'delete': 'destroy',
            
        })),
    path("posts/<pk>", PostViewSet.as_view({
            'get' : 'retrieve',
    })),
    path("posts/<pk>/like/", PostViewSet.as_view({
            'post' : 'like',
    })),
    path("comments/", CommentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'partial_update',
            'delete': 'destroy'
        })),
    path("profile_photo/", UploadUserPhotoViewSet.as_view(
        {
            'post': 'create',
        })),
    path("activate/<uid>/<token>/", ActivateUser.as_view()),

    path("users/me/", UsersMe.as_view({'get': 'list',})),
]