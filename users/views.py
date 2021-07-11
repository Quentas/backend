from pathlib import Path
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
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import (
    Post, 
    Comment, 
    Account,
    Picture,
)

from .serializers import (
    PostSerializer, 
    PostDetailSerializer,
    PostCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    CommentDetialSerializer,
    FileUploadSerializer,
    PictureSerializer,
)
from .service import modify_input_for_multiple_files as modify


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny,]
        endpos = None
        startpos = None
        queryset = Post.objects.all()
        # /posts/?username=admin
        if request.GET.get('username'):                                 
            queryset = Post.objects.filter(user__username=request.GET.get('username'))
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = PostSerializer(queryset.order_by("-date")[startpos:endpos], many=True)
        return Response(serializer.data)

    def create(self, request):      
        self.permission_classes = [IsAuthenticated,]
        if request.method == 'POST' and request.POST.get('content'):  # check if not empty
            data = request.POST
            post = Post.objects.create(user=request.user, content=request.data['content'])
            images = request.FILES.getlist('images')
            for image in images:
                if Path(str(image)).suffix in {'.jpg', '.jpeg', '.png'}:        
                    img_instance = Picture.objects.create(image=image)
                    post.images.add(img_instance)
            return Response(status=201)
        else:
            return Response(status=400)
                            
    def retrieve(self, request, pk=None):
        self.permission_classes = [AllowAny,]
        post = get_object_or_404(Post, id=int(pk))
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def partial_update(self, request):
        self.permission_classes = [IsAuthenticated,]
        post = get_object_or_404(Post, id=int(request.data["id"]))
        if request.user == post.user:
            post.content = request.data['content']
            #if request.data['images']:
            #    post.images = request.data['images']
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
        endpos = None
        startpos = None
        queryset = Comment.objects.all()
        # /comments/?username=admin
        if request.GET.get('username'):                                 
            queryset = Comment.objects.filter(user__username=request.GET.get('username'))
        # /comments/?comment_id=1
        # //// is this necessary ???
        if request.GET.get('comment_id'):                                           
            queryset = Comment.objects.filter(id=request.GET.get('comment_id'))
        # cuts list of objects
        if request.GET.get('endpos'):
            endpos = int(request.GET.get('endpos'))
        if request.GET.get('startpos'):
            startpos = int(request.GET.get('startpos'))
        serializer = CommentSerializer(queryset.order_by("-date")[startpos:endpos], many=True)
        return Response(serializer.data)
    '''
    def retrieve(self, request, pk=None):
        self.permission_classes = [AllowAny,]
        comment = get_object_or_404(Post, id=int(pk))
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    '''

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

    def partial_update(self, request):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=int(request.data["id"]))
        if request.user == comment.user:
            comment.content = request.data["content"]
            comment.save()
            return Response(status=200)
        else:
            return Response(status=403)

    def destroy(self, request):
        self.permission_classes = [IsAuthenticated,]
        comment = get_object_or_404(Comment, id=int(request.data["id"]))
        if request.user == comment.user:
            comment.delete()
            return Response(status=200)
        else:
            return Response(status=403)


class UploadUserPhotoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = FileUploadSerializer
    def create(self, request):
        file_uploaded = request.FILES.get('photo')
        file_extension = Path(str(file_uploaded)).suffix
        if file_extension in {'.jpg', '.jpeg', '.png'}:
            request.user.profile_photo = file_uploaded
            request.user.save()
            return Response(status=200)
        return Response(status=400)
   

class ActivateUser(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    def get(self, request, uid, token, format = None):
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


def index(request):
    return render(request, 'index.html')