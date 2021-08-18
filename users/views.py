from datetime import date, datetime, timedelta
import json
from os import stat
from pathlib import Path
from django.http.response import HttpResponse
from django.utils import timezone
import requests
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
)

from django.contrib.auth import login

from rest_framework import (
    generics, 
    permissions,
    viewsets, 
    serializers,
)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
)

from rest_framework.views import APIView

from .models import (
    Post, 
    Comment, 
    Account,
    Picture,
    
)

from .serializers import (
    DetailUserSerializer,
    PostSerializer, 
    PostDetailSerializer,
    PostCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    CommentDetialSerializer,
    FileUploadSerializer,
    PictureSerializer,
    UserDataUpdateSerializer,
)
from .service import is_stored_on_server as is_stored, modify_input_for_multiple_files as modify


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny,]
        endpos = None
        startpos = None
        queryset = Post.objects.all()
        # /posts/?username=admin
        if request.GET.get('username'):                                 
            queryset = queryset.filter(user__username=request.GET.get('username'))
        # /posts/?liked_by=admin
        if request.GET.get('liked_by'):
            queryset = queryset.filter(likes__username=request.GET.get('liked_by'))
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = PostSerializer(queryset.order_by("-pub_date")[startpos:endpos], 
                                        many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        self.permission_classes = [IsAuthenticated,]

        if request.method == 'POST' and request.data['content']:  # check if not empty
            images = request.FILES.getlist('image')
            if len(images) > 6: 
                return Response({"Image upload error": "Too many images uploaded. Maximum amount is 6"}, status=400)
            for image in images:  ##  fistly check all images
                if image.size > 2000000:  ## 2 MB
                    return Response({"Image upload error": "Too big images uploaded. Maximum size is 2 MB"}, status=400)
                if not Path(str(image)).suffix in {'.jpg', '.jpeg', '.png', '.gif'}:
                    return Response({"Image upload error": "Images of formats jpg, jpeg, png are supported"}, status=400)
            post = Post.objects.create(user=request.user, content=request.data['content'])
            for image in images:  
                img_instance = Picture.objects.create(image=image)
                post.images.add(img_instance)
            return Response(status=201)
        else:
            return Response({"Error": "No 'content' field or no POST request"}, status=400)
        #'''
                         
    def retrieve(self, request, pk):
        self.permission_classes = [AllowAny,]
        post = get_object_or_404(Post, id=pk)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
        
    def partial_update(self, request, pk=None):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            if not request.data['content'] or len(request.data['content'])==0:
                return Response({"Content error": "Post must contain 'content' field"}, status=400)
            old_images = post.images.values('id')
            old_images_count = post.images.all().count()
            deleted_imgs_count = 0
            img_list = [img['id'] for img in old_images]
            for img in request.POST.getlist('deleted'):   ## delete unwanted images
                if int(img) in img_list:
                    deleted_imgs_count += 1
                    post.images.get(id=img).delete()
            images = request.FILES.getlist('image')
            if len(images) + old_images_count - deleted_imgs_count > 6: 
                return Response({"Image upload error": "Too many images uploaded. Maximum amount is 6"}, status=400) 
            for image in images:  ##  fistly check all uploaded images
                if image.size > 2000000:  ## 2 MB
                    return Response({"Image upload error": "Too big images uploaded. Maximum size is 2 MB"}, status=400)
                if not Path(str(image)).suffix in {'.jpg', '.jpeg', '.png', '.gif'}:
                    return Response({"Image upload error": "Images of formats jpg, jpeg, png are supported"}, status=400)
            post.content = request.data['content']
            for image in images:  
                img_instance = Picture.objects.create(image=image)
                post.images.add(img_instance)
            post.save()
            return Response(status=200)
        return Response(status=403)

    def destroy(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            post.delete()
            return Response(status=200)
        else:
            return Response(status=403)
        
    def like(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(username=request.user).exists():
            post.likes.remove(request.user)
            return Response(status=204)
        post.likes.add(request.user)
        return Response(status=200)

    def bookmark(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=pk)
        if post.bookmark.filter(username=request.user).exists():
            post.bookmark.remove(request.user)
            return Response(status=204)
        post.bookmark.add(request.user)
        return Response(status=200)

    def my_bookmarks(self, request):
        self.permission_classes = [IsAuthenticated,]
        if not request.user.is_authenticated:
            return Response(status=403)
        queryset = request.user.booked_post.all()
        endpos = None
        startpos = None
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = PostSerializer(queryset.order_by("-pub_date")[startpos:endpos], 
                                        many=True, context={'request': request})
        return Response(serializer.data)

    def get_hot_posts(self, request):
        self.permission_classes = [AllowAny,]
        startpos = None
        endpos = None
        queryset = Post.objects.filter(pub_date__gte=datetime.now()-timedelta(days=3)).filter(likes__gt = 0)
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = PostSerializer(queryset.order_by("likes")[startpos:endpos], 
                                        many=True, context={'request': request})    
        return Response(serializer.data)

class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny,]
        endpos = None
        startpos = None
        queryset = Comment.objects.all()
        # /comments/?username=admin
        if request.GET.get('username'):                                 
            queryset = queryset.filter(user__username=request.GET.get('username'))
        # /comments/?post_id=1
        if request.GET.get('post_id'):                                           
            queryset = queryset.filter(post__id=request.GET.get('post_id'))
        # /comments/?parent_id=1
        if request.GET.get('parent_id'):
            if request.GET.get('parent_id') == 'null':                   
                queryset = queryset.filter(parent__id__isnull=True)
            else:
                queryset = queryset.filter(parent__id = request.GET.get('parent_id'))
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = CommentSerializer(queryset.order_by("-pub_date")[startpos:endpos], 
                                            many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        self.permission_classes = [AllowAny,]
        comment = get_object_or_404(Comment, id=int(pk))
        serializer = CommentDetialSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated,]
        parent_comment = None
        created_comment = CommentCreateSerializer(data=request.data)
        post_instance = get_object_or_404(Post, id=int(request.data["post"]))
        if request.data["parent"]:
            parent_comment = get_object_or_404(Comment, id=int(request.data["parent"]))
        if created_comment.is_valid():
            created_comment.save(user=request.user, post=post_instance, parent=parent_comment)
            return Response(status=201)
        else:
            return Response(status=400)

    def partial_update(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=pk)
        if not request.data['content']:
            return Response({"Content error" : "No content received"}, status=400)
        if request.user == comment.user:
            comment.content = request.data['content']
            comment.save()
            return Response(status=200)
        else:
            return Response(status=403)

    def destroy(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=pk)
        if request.user == comment.user:
            comment.delete()
            return Response(status=200)
        else:
            return Response(status=403)

    def like(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(username=request.user).exists():
            comment.likes.remove(request.user)
            return Response(status=204)
        comment.likes.add(request.user)
        return Response(status=200)

    def bookmark(self, request, pk):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=pk)
        if comment.bookmark.filter(username=request.user).exists():
            comment.bookmark.remove(request.user)
            return Response(status=204)
        comment.bookmark.add(request.user)
        return Response(status=200)

    def my_bookmarks(self, request):
        self.permission_classes = [IsAuthenticated,]
        if not request.user.is_authenticated:
            return Response(status=403)
        queryset = request.user.booked_comment.all()
        endpos = None
        startpos = None
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = PostSerializer(queryset.order_by("-pub_date")[startpos:endpos], 
                                        many=True, context={'request': request})
        return Response(serializer.data)

class UserDataViewSet(viewsets.ViewSet):

    def get(self, request, uid, token, format = None):
        """
        """
        self.permission_classes = [AllowAny,]
        payload = {'uid': uid, 'token': token}
        #url = "https://fierce-dusk-92502.herokuapp.com/auth/users/activation/"
        url = "http://127.0.0.1:8000/auth/users/activation/"
        response = requests.post(url, data = payload)
        if response.status_code == 204:
            #return Response({}, response.status_code)
            #return HttpResponseRedirect("https://fierce-dusk-92502.herokuapp.com")
            return HttpResponseRedirect("http://127.0.0.1:8000")
        else:
            return Response(response.json())

    def create(self, request):
        """Upload `user` avatar
        """
        self.permission_classes = [IsAuthenticated,]
        self.serializer_class = FileUploadSerializer
        if not request.FILES.getlist('photo'):
            return Response({"Image upload error" : "Image must be uploaded"}, status=400)            
        file_uploaded = request.FILES.getlist('photo')[0]
        if Path(str(file_uploaded)).suffix in {'.jpg', '.jpeg', '.png'}:
            request.user.profile_photo = file_uploaded
            request.user.save()
            return Response(status=200)
        return Response(status=400)


    def partial_update(self, request):
        """Update `user` fields `bio`, `first_name` and `last_name`
        """
        self.permission_classes = [IsAuthenticated,]
        serializer = UserDataUpdateSerializer(request.data)
        if serializer.is_valid:
            request.user.bio = serializer.data['bio']
            request.user.first_name = serializer.data['first_name']
            request.user.last_name = serializer.data['last_name']
            request.user.save()
            return Response(status=200)
        return Response(status=400)

from django.views import View
from django.http import JsonResponse

class RedirectSocial(View):

    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        return JsonResponse(json_obj)


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=200)
        except Exception as e:
            return Response(status=400)