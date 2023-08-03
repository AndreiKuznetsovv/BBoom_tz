"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from blog.views import UserPostsListAPIView, UserListAPIView, PostRetrieveUpdateDestroyAPIView, PostCreateAPIView, \
    UserCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1.0/auth/", include('rest_framework.urls')),
    path("api/v1.0/auth/register", UserCreateAPIView.as_view(), name="register"),
    path('api/v1.0/users/', UserListAPIView.as_view(), name="users"),
    path('api/v1.0/posts/', PostCreateAPIView.as_view(), name="create_post"),
    path('api/v1.0/posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view(), name="posts"),
    path('api/v1.0/users/<int:user>', UserPostsListAPIView.as_view(), name="user_posts")
]
