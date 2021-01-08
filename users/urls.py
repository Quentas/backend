from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.PostListView.as_view({'get': 'list'})),
    path("posts/create/", views.PostCreateView.as_view()),
]