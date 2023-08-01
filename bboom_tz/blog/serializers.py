from rest_framework.serializers import ModelSerializer
from .models import User, Post


class UserSerializer(ModelSerializer):


    class Meta:
        model = User
        fields = ('name', 'email')


class PostSerializer(ModelSerializer):


    class Meta:
        model = Post
        field = ('title', 'body', 'author')