import base64

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status, HTTP_HEADER_ENCODING

from blog.models import User
from .test_setup import TestSetUp


class TestUserCreateAPIView(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        """
        Ensure we cannot get register without user data.
        permission class: AllowAny
        Expected status code = 400.
        """

        response = self.client.post(self.register_url)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        """
        Ensure we cannot get register with correct user data.
        permission class: AllowAny
        Expected status code = 201.
        """

        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'test_user1')


class TestUserPostsListAPIView(TestSetUp):
    def test_unauthorized_user_can_get_posts(self):
        """
        Ensure we cannot get user posts.
        permission class: IsAuthorized
        Expected status code = 403.
        """

        # register a new user
        self.client.post(self.register_url, self.register_data, format='json')

        # set fake base64 credentials
        fake_base64_credentials = "fake credentials"

        # defining url to get user's posts
        user_posts_url = 'http://127.0.0.1:5000/api/v1.0/users/1'

        response = self.client.get(user_posts_url, HTTP_AUTHORIZATION=f"{fake_base64_credentials}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_get_posts(self):
        """
        Ensure we can get user posts.
        permission class: IsAuthorized
        Expected status code = 200.
        """

        # register a new user
        self.client.post(self.register_url, self.register_data, format='json')

        # Generate base64 credentials string
        credentials = f"{self.login_data['username']}:{self.login_data['password']}"
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)

        # defining url to get user's posts
        user_posts_url = 'http://127.0.0.1:5000/api/v1.0/users/1'

        response = self.client.get(user_posts_url, HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserListAPIView(TestSetUp):
    def test_superuser_can_get_users_list(self):
        """
        Ensure we can get users list.
        permission class: IsAdminUser
        Expected status code = 200.
        """

        # creating SUPERUSER user
        UserModel = get_user_model()
        UserModel.objects.create_superuser(
            username=self.register_data['username'],
            name=self.register_data['name'],
            email=self.register_data['email'],
            password=self.register_data['password']
        )

        users_list_url = reverse("users")

        # Generate base64 credentials string
        credentials = f"{self.login_data['username']}:{self.login_data['password']}"
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)

        response = self.client.get(users_list_url, HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_superuser_can_get_users_list(self):
        """
        Ensure we cannot get users list without ADMIN rights.
        permission class: IsAdminUser
        Expected status code = 403.
        """

        # register a new NOT SUPERUSER user
        self.client.post(self.register_url, self.register_data, format='json')

        # Generate base64 credentials string
        credentials = f"{self.login_data['username']}:{self.login_data['password']}"
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        # defining url to get users list
        users_list_url = reverse("users")

        response = self.client.get(users_list_url, HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
