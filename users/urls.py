from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,

)

urlpatterns = [
    path("posts/", PostListView.as_view({'get': 'list'})),
    path("posts/create/", PostCreateView.as_view()),
    path("posts/delete/", PostDeleteView.as_view()),
    path("posts/update/", PostUpdateView.as_view()),
    path("posts/create_comment/", CommentCreateView.as_view()),
    path("posts/delete_comment/", CommentDeleteView.as_view()),
    path("posts/update_comment/", CommentUpdateView.as_view()),

]