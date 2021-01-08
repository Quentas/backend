from django.shortcuts import render
from django.http import HttpRequest
from rest_framework import generics, permissions, viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
#from knox.models import AuthToken   
from .models import Post
from .serializers import UserSerializer, RegisterSerializer, PostSerializer, PostCreateSerializer
from rest_framework.permissions import IsAuthenticated


'''             
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]							###########################
        })

'''

class PostListView(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('user_id'):                                  # http://127.0.0.1:8000/api/v1/posts/?user_id=admin
            user_id = request.GET.get('user_id')
            queryset = Post.objects.filter(user__id=user_id)
        elif request.GET.get('username'):                               # http://127.0.0.1:8000/api/v1/posts/?username=admin
            username = request.GET.get('username')            
            queryset = Post.objects.filter(user__username=username)
        elif request.GET.get('post_id'):                                # http://127.0.0.1:8000/api/v1/posts/?post_id=admin
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
            created_post.save(user = request.user)
            return Response(status=201)
        else:
            return Response(status=400)

