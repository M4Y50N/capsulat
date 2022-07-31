from datetime import datetime
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Classe(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    room_join = models.CharField(default='room', max_length=20)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)

    date_control_initial = models.DateField(default=datetime.today, null=False)
    date_control_end = models.DateField(blank=True, null=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    created_in = models.TextField(blank=True)
    crypt_key = models.CharField(default='capsulat',  max_length=23)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    created_in = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.body[0:50]
