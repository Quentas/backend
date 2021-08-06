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
    class Meta:
        model = Account
        fields = objUserSerializer.Meta.fields + ('bio',)
        read_only_fields = fields        


class UserBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('bio',)


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image',)
        

class objSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    comments_count = serializers.ReadOnlyField()
    user = objUserSerializer(read_only=True)
    is_fan = SerializerMethodField()
    is_booked = SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    class Meta:
        fields = ('id', 'user', 'content', 'date', 
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
        model.date = serializers.DateTimeField()
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
        model.date = serializers.DateTimeField() 
        fields = ['content', 'images',]
        #fields = ['content',]

    ## write create method and _validateImages_ method


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_photo',)


class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']