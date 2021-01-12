from rest_framework import serializers
from .models import (
    Account, 
    Post,
)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Post
        fields = ("id", "user", "content", "date")


class PostCreateSerializer(serializers.ModelSerializer): #change fields
    class Meta:
        model = Post
        #fields = "__all__"
        model.date = serializers.DateTimeField()  #this works
        #fields = ["id", "user", "content"]
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