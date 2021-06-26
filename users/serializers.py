from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from .models import (
    Account, 
    Post,
    Comment,
    Picture
)

class PartialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'profile_photo' ,'first_name', 'last_name']
        read_only_fields = fields


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image',)
        

class CommentSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    user = PartialUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'date', 'last_edited', 'images', 'post',)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        model.date = serializers.DateTimeField()
        fields = ["post", "content"]


class PostSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    user = PartialUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'date', 'last_edited', 'images',)   


class PostCreateSerializer(serializers.ModelSerializer): 
    images = PictureSerializer(many=True)
    class Meta:
        model = Post
        model.date = serializers.DateTimeField() 
        fields = ['content', 'images',]
        #fields = ['content',]


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'user_permissions', 'is_superuser')


class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']