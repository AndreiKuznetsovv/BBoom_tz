from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(default="Без названия", max_length=100)
    body = models.TextField(blank=True, max_length=500)
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
