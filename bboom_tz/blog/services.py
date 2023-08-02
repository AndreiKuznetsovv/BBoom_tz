from typing import Type

from django.db import DatabaseError
from rest_framework.exceptions import ValidationError

from .models import Post, User
from .serializers import PostSerializer, UserSerializer


def get_users_list() -> tuple[int, dict]:
    try:
        users_list = User.objects.all()
    except Exception as exc:
        return 500, {"error": "Unable to get users data"}
    return 200, UserSerializer(users_list, many=True).data


def get_user_posts(author_id: int) -> tuple[int, dict]:
    try:
        user_posts = Post.objects.filter(author_id=author_id).all()
    except Exception as exc:
        return 422, {"error": "Unable to get user with this id"}
    return 200, PostSerializer(user_posts, many=True).data


def is_exists(model: Type[Post | User], pk: id) -> Post | bool:
    try:
        instance = model.objects.get(id=pk)
    except Post.DoesNotExist as exc:
        return False
    return instance


def create_post(data: dict) -> tuple[int, dict]:
    try:
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return 422, {"error": "Unable to validate given data"}
    try:
        new_post = Post.objects.create(**data)
    except DatabaseError as e:
        return 422, {"error": "Unable to create post with given data"}

    return 201, PostSerializer(new_post).data


def update_post(data: dict, post_id: int) -> tuple[int, dict]:
    instance = is_exists(model=Post, pk=post_id)
    if not instance:
        return 404, {"error": "Object does not exists"}
    else:
        try:
            validated_data = PostSerializer(data=data)
            validated_data.is_valid(raise_exception=True)
        except ValidationError as exc:
            return 422, {"error": "Unable to validate given data"}
        instance.title = validated_data.data.get("title", instance.title)
        instance.body = validated_data.data.get("body", instance.body)
        instance.author_id = validated_data.data.get("author_id", instance.author_id)
        try:
            instance.save()
        except  DatabaseError:
            return 422, {"error": "Unable to update post with given data"}
        return 200, PostSerializer(instance).data


def delete_post(post_id: int) -> tuple[int, dict | None]:
    instance = is_exists(model=Post, pk=post_id)
    if not instance:
        return 404, {"error": "Object does not exists"}

    try:
        instance.delete()
    except  DatabaseError:
        return 422, {"error": "Unable to delete post"}
    return 204, None
