from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from .models import User, Post


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")


class PostSerializer(ModelSerializer):
    """Creating hidden field for current user. Using in permission functionality"""
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("title", "body", "user")
