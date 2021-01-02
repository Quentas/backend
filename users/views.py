from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
#from knox.models import AuthToken   
from .models import Post
from .serializers import UserSerializer, RegisterSerializer, PostSerializer



# Register API
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

class PostListView(APIView):
    
    def get(self, request):
        posts = Post.objects.order_by("-date")
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

