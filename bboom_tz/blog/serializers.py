from rest_framework.serializers import ModelSerializer, CharField, IntegerField, Serializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')


class PostSerializer(Serializer):
    title = CharField(max_length=100)
    body = CharField(max_length=500)
    author_id = IntegerField()
