from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = "http://127.0.0.1:5000/api/v1.0/auth/login/"

        self.register_data = {
            "name": "test_user1",
            "username": "test_user1",
            "email": "test_user1@gmail.com",
            "password": "test"
        }

        self.login_data = {
            "username": self.register_data.get("username"),
            "password": self.register_data.get("password")
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

