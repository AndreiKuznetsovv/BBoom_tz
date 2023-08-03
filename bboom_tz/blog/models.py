from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100, null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(default="Без названия", max_length=100)
    body = models.TextField(blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title
