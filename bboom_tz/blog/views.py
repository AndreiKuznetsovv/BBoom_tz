from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import User, Post
from .serializers import UserSerializer, PostSerializer


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class PostAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer