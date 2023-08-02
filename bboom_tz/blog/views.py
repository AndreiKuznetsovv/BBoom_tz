from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import create_post, get_users_list, get_user_posts, update_post, delete_post


class UserAPIView(APIView):
    def get(self, request: Request) -> Response:
        status, data = get_users_list()  # unpacking tuple[int, dict]
        return Response(status=status, data={"users": data})


class UserPostsAPIView(APIView):

    def get(self, request: Request, user_id: int) -> Response:
        status, data = get_user_posts(author_id=user_id)  # unpacking tuple[int, dict]
        return Response(status=status, data={"user posts": data})


class PostAPIView(APIView):
    def post(self, request: Request) -> Response:
        status, data = create_post(data=request.data)
        return Response(status=status, data={"created post": data})

    def put(self, request: Request, post_id: int) -> Response:
        status, data = update_post(data=request.data, post_id=post_id)
        return Response(status=status, data={"updated post": data})

    def delete(self, request: Request, post_id: int) -> Response:
        status, data = delete_post(post_id=post_id)

        return Response(status=204, data=data)
