from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Post
from .serializers import UserSerializer, PostSerializer


class UserAPIView(APIView):
    def get(self, request: Request) -> Response:
        users_list = User.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(status=200, data={"users": serializer.data})


class UserPostsAPIView(APIView):

    def get(self, request: Request, user_id: int) -> Response:
        user_posts = Post.objects.filter(author_id=user_id).all()
        serializer = PostSerializer(user_posts, many=True)
        return Response(status=200, data={"user posts": serializer.data})


class PostAPIView(APIView):
    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(status=200, data={"posts": serializer.data})

    def post(self, request: Request) -> Response:
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201, data={"post info": serializer.data})

    def put(self, request: Request, post_id: int) -> Response:
        try:
            instance = Post.objects.get(id=post_id)
        except Post.DoesNotExist as e:
            return Response(status=404, data={"error": "Object does not exists"})

        serializer = PostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200, data={"updated post": serializer.data})

    def delete(self, request: Request, post_id: int) -> Response:
        try:
            instance = Post.objects.get(id=post_id)
        except Post.DoesNotExist as e:
            return Response(status=404, data={"error": "Object does not exists"})

        instance.delete()

        return Response(status=204)
