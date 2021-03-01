import pathlib
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

from .models import (
    Post, 
    Comment, 
    Account,
)
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    FileUploadSerializer,
)


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny,]
        # /posts/?user_id=1
        if request.GET.get('user_id'):                                  
            user_id = request.GET.get('user_id')
            queryset = Post.objects.filter(user__id=user_id)
        # /posts/?username=admin
        elif request.GET.get('username'):                               
            username = request.GET.get('username')            
            queryset = Post.objects.filter(user__username=username)
        # /posts/?post_id=1
        elif request.GET.get('post_id'):                                
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
        # /comments/?user_id=1
        if request.GET.get('user_id'):                                  
            user_id = request.GET.get('user_id')
            queryset = Comment.objects.filter(user__id=user_id)
        # /comments/?username=admin
        elif request.GET.get('username'):                               
            username = request.GET.get('username')            
            queryset = Comment.objects.filter(user__username=username)
        # /comments/?comment_id=1
        elif request.GET.get('comment_id'):                                
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


class UploadViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = FileUploadSerializer
    def create(self, request):
        file_uploaded = request.FILES.get('photo')
        file_extension = pathlib.Path(str(file_uploaded)).suffix
        user_instance = Account.objects.get(username=request.user)
        if file_extension in {'.jpg', '.jpeg', '.png'}:
            user_instance.profile_photo = file_uploaded
            user_instance.save()
            return Response(status=200)
        return Response(status=400)
