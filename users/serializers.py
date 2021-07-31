from rest_framework.fields import SerializerMethodField
from users.service import is_fan
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
    comments_count = serializers.ReadOnlyField(source='count_replies')
    user = PartialUserSerializer(read_only=True)
    is_fan = SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ('id', 'post', 'parent', 'user', 'content', 'date', 
        'last_edited', 'images', 'comments_count', 'is_fan', 'total_likes',)

    def get_is_fan(self, obj):
        user = self.context['request'].user
        return is_fan(obj, user)


class CommentDetialSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    user = PartialUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'parent', 'user', 'content', 'date', 'last_edited', 'images',)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        model.date = serializers.DateTimeField()
        fields = ["post", "content"]


class PostSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    user = PartialUserSerializer(read_only=True)
    total_likes = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField(source='count_replies')
    is_fan = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'date', 'last_edited',
         'images', 'comments_count', 'total_likes', 'is_fan', )   
    
    def get_is_fan(self, obj):
        user = self.context['request'].user
        return is_fan(obj, user)


class PostDetailSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    user = PartialUserSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField(source='count_replies')
    total_likes = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True)
    is_fan = SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'date', 'last_edited', 'images', 
        'comments_count', 'comments', 'total_likes', 'is_fan', ) 

    def get_is_fan(self, obj):
        user = self.context['request'].user
        return is_fan(obj, user)
          
    
class PostCreateSerializer(serializers.ModelSerializer): 
    #images = PictureSerializer(many=True)
    class Meta:
        model = Post
        model.date = serializers.DateTimeField() 
        #fields = ['content', 'images',]
        fields = ['content',]

    ## write create method and _validateImages_ method


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_photo',)


class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']