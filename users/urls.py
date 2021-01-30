from django.urls import path
from .views import (
    PostViewSet,
    CommentViewSet,
)

urlpatterns = [
    path("posts/", PostViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'partial_update',
            'delete': 'destroy'
        })),
    path("comments/", CommentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'partial_update',
            'delete': 'destroy'
        })),

]