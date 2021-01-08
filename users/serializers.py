from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Post

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


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