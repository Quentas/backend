from rest_framework import serializers
from .models import (
    Account, 
    Post,
    Comment,
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
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "content", "date", "last_edited")
#'''

class PostIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',)



class PostCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Post
        model.date = serializers.DateTimeField() 
        fields = ["content"]
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password, ')

class PartialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name',
                 'is_active', 'is_staff', 'profile_photo', ]
        extra_kwargs  = {
            'username' : {'read_only' : True},
            'email' : {'read_only' : True},
            'first_name' : {'read_only' : True},
            'last_name' : {'read_only' : True},
            'is_active' : {'read_only' : True},
            'is_staff' : {'read_only' : True},
            'profile_photo' : {'read_only' : True},
            
        }

class FileUploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']