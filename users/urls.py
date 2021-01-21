from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    CommentCreateView,
)

urlpatterns = [
    path("posts/", PostListView.as_view({'get': 'list'})),
    path("posts/create/", PostCreateView.as_view()),
    path("posts/create_comment/", CommentCreateView.as_view()),
]