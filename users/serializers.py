from rest_framework import serializers
from .models import (
    Account, 
    Post,
    Comment,
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "user", "content", "date")


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

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Post
        fields = ("id", "user", "content", "date", "comments")


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