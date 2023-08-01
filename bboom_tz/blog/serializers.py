from rest_framework.serializers import ModelSerializer, CharField, IntegerField, Serializer

from .models import User, Post


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')


class PostSerializer(Serializer):
    title = CharField(max_length=100)
    body = CharField(max_length=500)
    author_id = IntegerField()

    def create(self, validated_data: dict) -> Post:
        return Post.objects.create(**validated_data)

    def update(self, instance: Post, validated_data: dict):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.save()
        print(type(instance))
        return instance

