from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Sala(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sala', null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Participante(models.Model):
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    part = models.CharField(max_length=200)

    def __str__(self):
        return self.text
