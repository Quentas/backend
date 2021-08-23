from datetime import date, datetime, timedelta
from pathlib import Path
import requests

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Post,
    Comment,
    Account,
    Picture,
)
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    CommentDetialSerializer,
    FileUploadSerializer,
    UserDataUpdateSerializer,
    SocialAuthSerializer,
    CustomTokenObtainPairSerializer
)
from .service import password_generate, validate_images


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny, ]
        queryset = Post.objects.all()
        # /posts/?username=admin
        if request.GET.get('username'):
            queryset = queryset.filter(
                user__username=request.GET.get('username')
                )
        # /posts/?liked_by=admin
        if request.GET.get('liked_by'):
            queryset = queryset.filter(
                likes__username=request.GET.get('liked_by')
                )
        # cuts list of objects
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = PostSerializer(
            queryset.order_by("-pub_date")[startpos:endpos],
            many=True, context={'request': request}
            )
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated, ]
        if request.method == 'POST' and request.data['content']:  # check if not empty
            images = request.FILES.getlist('image')
            images_valid = validate_images(images)
            if images_valid is not True:
                return images_valid
            post = Post.objects.create(user=request.user, content=request.data['content'])
            for image in images:
                img_instance = Picture.objects.create(image=image)
                post.images.add(img_instance)
            return Response(status=201)
        else:
            return Response({"detail": "No 'content' field or no POST request"}, status=400)

    def retrieve(self, request, pk):
        self.permission_classes = [AllowAny, ]
        post = get_object_or_404(Post, id=pk)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        self.permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            if not request.data['content'] or len(request.data['content']) == 0:
                return Response({"detail": "Post must contain 'content' field"}, status=400)
            old_images = post.images.values('id')
            old_images_count = post.images.all().count()
            deleted_imgs_count = 0
            img_list = [img['id'] for img in old_images]
            for img in request.POST.getlist('deleted'):   # delete unwanted images
                if int(img) in img_list:
                    deleted_imgs_count += 1
                    post.images.get(id=img).delete()
            images = request.FILES.getlist('image')
            if len(images) + old_images_count - deleted_imgs_count > 6:
                return Response({"detail": "Too many images uploaded. Maximum amount is 6"}, status=400)
            images_valid = validate_images(images)
            if images_valid is not True:
                return images_valid
            post.content = request.data['content']
            for image in images:
                img_instance = Picture.objects.create(image=image)
                post.images.add(img_instance)
            post.save()
            return Response(status=200)
        return Response(status=403)

    def destroy(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            post.delete()
            return Response(status=200)
        else:
            return Response(status=403)

    def like(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(username=request.user).exists():
            post.likes.remove(request.user)
            return Response(status=204)
        post.likes.add(request.user)
        return Response(status=200)

    def bookmark(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(Post, id=pk)
        if post.bookmark.filter(username=request.user).exists():
            post.bookmark.remove(request.user)
            return Response(status=204)
        post.bookmark.add(request.user)
        return Response(status=200)

    def my_bookmarks(self, request):
        self.permission_classes = [IsAuthenticated, ]
        if not request.user.is_authenticated:
            return Response(status=403)
        queryset = request.user.booked_post.all()
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = PostSerializer(queryset.order_by("-pub_date")[startpos:endpos],
                                    many=True, context={'request': request})
        return Response(serializer.data)

    def get_hot_posts(self, request):
        self.permission_classes = [AllowAny, ]
        queryset = Post.objects.filter(pub_date__gte=datetime.now()-timedelta(days=3)).filter(likes__gt=0)
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = PostSerializer(queryset.order_by("likes")[startpos:endpos],
                                    many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        self.permission_classes = [AllowAny, ]
        queryset = Comment.objects.all()
        # /comments/?username=admin
        if request.GET.get('username'):
            queryset = queryset.filter(user__username=request.GET.get('username'))
        # /comments/?post_id=1
        if request.GET.get('post_id'):
            queryset = queryset.filter(post__id=request.GET.get('post_id'))
        # /comments/?liked_by=admin
        if request.GET.get('liked_by'):
            queryset = queryset.filter(likes__username=request.GET.get('liked_by'))
        # /comments/?parent_id=1
        if request.GET.get('parent_id'):
            if request.GET.get('parent_id') == 'null':
                queryset = queryset.filter(parent__id__isnull=True)
            else:
                queryset = queryset.filter(parent__id=request.GET.get('parent_id'))
        # cuts list of objects
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = CommentSerializer(queryset.order_by("-pub_date")[startpos:endpos],
                                       many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        self.permission_classes = [AllowAny, ]
        comment = get_object_or_404(Comment, id=int(pk))
        serializer = CommentDetialSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        self.permission_classes = [IsAuthenticated, ]
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
        self.permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(Comment, id=pk)
        if not request.data['content']:
            return Response({"detail": "No content received"}, status=400)
        if request.user == comment.user:
            comment.content = request.data['content']
            comment.save()
            return Response(status=200)
        else:
            return Response(status=403)

    def destroy(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(Comment, id=pk)
        if request.user == comment.user:
            comment.delete()
            return Response(status=200)
        else:
            return Response(status=403)

    def like(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(username=request.user).exists():
            comment.likes.remove(request.user)
            return Response(status=204)
        comment.likes.add(request.user)
        return Response(status=200)

    def bookmark(self, request, pk):
        self.permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(Comment, id=pk)
        if comment.bookmark.filter(username=request.user).exists():
            comment.bookmark.remove(request.user)
            return Response(status=204)
        comment.bookmark.add(request.user)
        return Response(status=200)

    def my_bookmarks(self, request):
        self.permission_classes = [IsAuthenticated, ]
        if not request.user.is_authenticated:
            return Response(status=403)
        queryset = request.user.booked_comment.all()
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = CommentSerializer(queryset.order_by("-pub_date")[startpos:endpos],
                                       many=True, context={'request': request}
                                       )
        return Response(serializer.data)


class UserDataViewSet(viewsets.ViewSet):

    def activate(self, request, uid, token, format=None):
        self.permission_classes = [AllowAny, ]
        payload = {'uid': uid, 'token': token}
        url = "http://127.0.0.1:8000/auth/users/activation/"
        response = requests.post(url, data=payload)
        if response.status_code == 204:
            return HttpResponseRedirect("http://127.0.0.1:8000")
        else:
            return Response(response.json())

    def avatar_upload(self, request):
        """Upload `user` avatar
        """
        self.permission_classes = [IsAuthenticated, ]
        self.serializer_class = FileUploadSerializer
        if not request.FILES.getlist('photo'):
            return Response({"detail": "Image must be uploaded"}, status=400)
        file_uploaded = request.FILES.getlist('photo')[0]
        if Path(str(file_uploaded)).suffix in {'.jpg', '.jpeg', '.png'}:
            request.user.profile_photo = file_uploaded
            request.user.save()
            return Response(status=200)
        return Response(status=400)

    def data_update(self, request):
        """Update `user` fields `bio`, `first_name` and `last_name`
        """
        self.permission_classes = [IsAuthenticated, ]
        serializer = UserDataUpdateSerializer(request.data)
        if serializer.is_valid:
            request.user.bio = serializer.data['bio']
            request.user.first_name = serializer.data['first_name']
            request.user.last_name = serializer.data['last_name']
            request.user.save()
            return Response(status=200)
        return Response(status=400)

    def get_subscriptions(self, request):
        self.permission_classes = [IsAuthenticated, ]
        if request.user.is_anonymous:
            return Response(status=401)
        if request.user.subscribed_to.count() == 0:
            return Response({"detail": "You have no subscriptions yet"}, status=400)
        queryset = Post.objects.filter(user__in=request.user.subscribed_to.all())
        endpos = int(request.GET.get('endpos')) if request.GET.get('endpos') else None
        startpos = int(request.GET.get('startpos')) if request.GET.get('startpos') else None
        serializer = PostSerializer(queryset.order_by("-pub_date")[startpos:endpos],
                                    many=True, context={'request': request})
        return Response(serializer.data)

    def subscribe(self, request, uname):
        self.permission_classes = [IsAuthenticated, ]
        if request.user.is_anonymous:
            return Response(status=401)
        if not uname:
            return Response(status=400)
        user_instance = get_object_or_404(Account, username=uname)
        if user_instance == request.user:
            return Response({"detail": "You cannot subscribe to yourself"}, status=400)
        if user_instance in request.user.subscribed_to.all():
            request.user.subscribed_to.remove(user_instance)
            return Response(status=204)
        request.user.subscribed_to.add(user_instance)
        return Response(status=200)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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


class SocialLogin(viewsets.ViewSet):

    def create(self, request):
        serializer = SocialAuthSerializer(data=request.data)
        if serializer.is_valid():
            if not request.data['id_token'] or not request.data['username'] or not request.data['email']:
                return Response({"detail": "SOSI"}, status=400)
            if Account.objects.filter(id_token=request.data['id_token']).count() > 0:
                return Response({"detail": "User with this id_token already exists"}, status=400)
            if Account.objects.filter(email=request.data['email']).count() > 0:
                return Response({"detail": "User with this email already exists"}, status=400)
            if Account.objects.filter(username=request.data['username']).count() > 0:
                return Response({"detail": "User with username '{}' already exists".format(request.data['username'])}, status=400)
            generated_password = password_generate(20)
            user = Account.objects.create(username=request.data['username'],
                                          email=request.data['email'],
                                          id_token=request.data['id_token'],
                                          )
            user.set_password(generated_password)
            user.save()
            return Response(status=200)
        return Response(serializer.data, status=400)

    def log_in(self, request):
        if not request.data['id_token'] or not request.data['email']:
            return Response({"detail": "SOSI"}, status=400)
        if Account.objects.filter(id_token=request.data['id_token']).filter(email=request.data['email']).count() > 0:
            queryset = Account.objects.filter(id_token=request.data['id_token'])
            user = queryset.get(email=request.data['email'])
            refresh = RefreshToken.for_user(user)
            return JsonResponse({"refresh": str(refresh)}, status=200)
        return Response({"detail": "No account with provided data"}, status=400)
