from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import HttpRequest
from django.contrib.auth import login

from rest_framework import (
    generics, 
    permissions,
    viewsets, 
    serializers,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
)
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny, ]
        if request.GET.get('user_id'):                                  
            # http://127.0.0.1:8000/api/v1/posts/?user_id=1
            user_id = request.GET.get('user_id')
            queryset = Post.objects.filter(user__id=user_id)
        elif request.GET.get('username'):                               
            # http://127.0.0.1:8000/api/v1/posts/?username=admin
            username = request.GET.get('username')            
            queryset = Post.objects.filter(user__username=username)
        elif request.GET.get('post_id'):                                
            # http://127.0.0.1:8000/api/v1/posts/?post_id=1
            post_id = request.GET.get('post_id')            
            queryset = Post.objects.filter(id=post_id)
        else:
            queryset = Post.objects.all()
        serializer = PostSerializer(queryset.order_by("-date"), many = True)
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated,]
        created_post = PostCreateSerializer(data=request.data)
        if created_post.is_valid():
            created_post.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=int(request.data["id"]))
        if request.user == post.user:
            post.content = request.data["content"]
            post.save()
            return Response(status=200)
        else:
            return Response(status=403)

    def destroy(self, request):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=int(request.data["id"]))
        if request.user == post.user:
            post.delete()
            return Response(status=200)
        else:
            return Response(status=403)


class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny,]
        if request.GET.get('user_id'):                                  
            # http://127.0.0.1:8000/api/v1/comments/?user_id=1
            user_id = request.GET.get('user_id')
            queryset = Comment.objects.filter(user__id=user_id)
        elif request.GET.get('username'):                               
            # http://127.0.0.1:8000/api/v1/comments/?username=admin
            username = request.GET.get('username')            
            queryset = Comment.objects.filter(user__username=username)
        elif request.GET.get('comment_id'):                                
            # http://127.0.0.1:8000/api/v1/comments/?comment_id=1
            comment_id = request.GET.get('comment_id')            
            queryset = Comment.objects.filter(id=comment_id)
        else:
            queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset.order_by("-date"), many = True)
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated,]
        created_comment = CommentCreateSerializer(data=request.data)
        post_instance = get_object_or_404(Post, id=int(request.data["post"]))
        if created_comment.is_valid():
            created_comment.save(user=request.user, post=post_instance)
            return Response(status=201)
        else:
            return Response(status=400)

    def destroy(self, request):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=int(request.data["id"]))
        if request.user == comment.user:
            comment.delete()
            return Response(status=200)
        else:
            return Response(status=403)

    def partial_update(self, request):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=int(request.data["id"]))
        if request.user == comment.user:
            comment.content = request.data["content"]
            comment.save()
            return Response(status=200)
        else:
            return Response(status=403)