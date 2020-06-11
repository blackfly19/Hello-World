from django.db import models

# Create your models here.


class User(models.Model):

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Chat(models.Model):

    username = models.CharField(max_length=100)
    message = models.CharField(max_length=100000000)

    def __str__(self):
        return str(self.id)