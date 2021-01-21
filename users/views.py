from django.shortcuts import render
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
    AllowAny
)
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import Post
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    CommentCreateSerializer
)


class PostListView(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    
    def list(self, request):
        if request.GET.get('user_id'):                                  
            # http://127.0.0.1:8000/api/v1/posts/?user_id=admin
            user_id = request.GET.get('user_id')
            queryset = Post.objects.filter(user__id=user_id)
        elif request.GET.get('username'):                               
            # http://127.0.0.1:8000/api/v1/posts/?username=admin
            username = request.GET.get('username')            
            queryset = Post.objects.filter(user__username=username)
        elif request.GET.get('post_id'):                                
            # http://127.0.0.1:8000/api/v1/posts/?post_id=admin
            post_id = request.GET.get('post_id')            
            queryset = Post.objects.filter(id=post_id)
        else:
            queryset = Post.objects.all()
        serializer = PostSerializer(queryset.order_by("-date"), many = True)
        return Response(serializer.data)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        created_post = PostCreateSerializer(data=request.data)
        if created_post.is_valid():
            created_post.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, post_id):
        '''
        try:
		    post = Post.objects.get(id = post_id)
	    except:
		    return Response(status=404)
        '''    
        created_comment = CommentCreateSerializer(data=request.data)
        if created_comment.is_valid():
           # created_comment.post = post
            created_comment.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)

