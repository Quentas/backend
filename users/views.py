from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
#from knox.models import AuthToken   
from .models import Post
from .serializers import UserSerializer, RegisterSerializer, PostSerializer


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
        queryset = Post.objects.all().order_by("-date")
        serializer = PostSerializer(queryset, many = True)
        return Response(serializer.data)

    def retrieve_user_id(self, request, pk=None):
        queryset = Post.objects.filter(user=pk).order_by("-date")
        serializer = PostSerializer(queryset, many = True)
        return Response(serializer.data)

    def retrieve_username(self, request, username=None):
        queryset = Post.objects.filter(user=username).order_by("-date")
        serializer = PostSerializer(queryset, many = True)
        return Response(serializer.data)

    def retrieve_post(self, request, pk=None):
        queryset = Post.objects.filter(id=pk).order_by("-date")
        serializer = PostSerializer(queryset, many = True)
        return Response(serializer.data)

