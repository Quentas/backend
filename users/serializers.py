from django.db.migrations.operations import fields
from rest_framework.fields import SerializerMethodField
from users.service import is_booked, is_fan
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from .models import (
    Account, 
    Post,
    Comment,
    Picture
)


class objUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'profile_photo' ,'first_name', 'last_name',)
        read_only_fields = fields


class PartialUserSerializer(objUserSerializer):
    user_posts_count = serializers.ReadOnlyField()
    user_comments_count = serializers.ReadOnlyField()
    user_likes_count = serializers.ReadOnlyField()
    class Meta:
        model = Account
        fields = objUserSerializer.Meta.fields + ('bio', 'user_posts_count', 'user_comments_count', 'user_likes_count',)
        read_only_fields = fields        


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_photo', 'bio',)


class UserDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('bio', 'first_name', 'last_name',)


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'image',)
        

class objSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    comments_count = serializers.ReadOnlyField()
    user = objUserSerializer(read_only=True)
    is_fan = SerializerMethodField()
    is_booked = SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    class Meta:
        fields = ('id', 'user', 'content', 'pub_date', 
        'last_edited', 'images', 'comments_count', 'is_fan', 'total_likes', 'is_booked',)

    def get_is_fan(self, obj):
        user = self.context['request'].user
        return is_fan(obj, user)

    def get_is_booked(self, obj):
        user = self.context['request'].user
        return is_booked(obj, user)
    


class CommentSerializer(objSerializer):
    class Meta:
        model = Comment
        fields = objSerializer.Meta.fields + ('post', 'parent', )


class CommentDetialSerializer(objSerializer):
    class Meta:
        model = Comment
        fields = objSerializer.Meta.fields + ('post', 'parent', )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        model.pub_date = serializers.DateTimeField()
        fields = ["post", "content"]


class PostSerializer(objSerializer):
    class Meta:
        model = Post
        fields = objSerializer.Meta.fields


class PostDetailSerializer(objSerializer):
    class Meta:
        model = Post
        fields = objSerializer.Meta.fields

    
class PostCreateSerializer(serializers.ModelSerializer): 
    images = PictureSerializer(many=True)
    class Meta:
        model = Post
        model.pub_date = serializers.DateTimeField() 
        fields = ['content', 'images',]
        #fields = ['content',]

    ## write create method and _validateImages_ method


class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']