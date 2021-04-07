from rest_framework import serializers
from .models import (
    Account, 
    Post,
    Comment,
    Picture
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        model.date = serializers.DateTimeField()
        fields = ["post", "content"]
'''
        Request be like:
        {
            "post": post_id,
            "content" : "smth"
        }
        
        And answer be like:
        {
            "id": <comment_id>,
            "post": <post_id>,
            "user": <username, who requested>,
            "content": "smth",
            "date": <post_date>
        }
    '''
'''
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Post
        fields = ("id", "user", "content", "date", "comments")
        
'''

class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('image',)

class PostSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'date', 'last_edited', 'images',)   

class PostIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',)

class PostCreateSerializer(serializers.ModelSerializer): 
    images = PictureSerializer(many=True)
    class Meta:
        model = Post
        model.date = serializers.DateTimeField() 
        fields = ['content', 'images',]
        #fields = ['content',]

'''
        Request be like:
        {
            "content" : "smth"
        }
        
        And answer be like:
        {
            "id": <post_id>,
            "user": <username, who requested>,
            "content": "smth",
            "date": <post_date>
        }
    '''

class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'user_permissions', 'is_superuser')

class PartialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'profile_photo']
        read_only_fields = fields

class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']