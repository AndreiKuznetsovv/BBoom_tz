from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, CharField

from .models import User, Post


class UserSerializer(ModelSerializer):
    """
    Maps the User model. Returning serialized fields: name, email.
    """

    password = CharField(write_only=True)
    username = CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ("name", "email", 'password', 'username')


class PostSerializer(ModelSerializer):
    """
    Maps the Post model. Returning serialized fields: title, body.
    Field user - Creating hidden field for current user. Required to set permissions.
    """
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("title", "body", "user")
