from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.


def randHex():
    hex_string = '0123456789abcdef'
    return ''.join([random.choice(hex_string) for x in range(5)])


class Sala(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sala', null=True)
    name = models.CharField(max_length=200)
    chave = models.CharField(max_length=5, default=randHex())

    def __str__(self):
        return self.name


class Participante(models.Model):
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    part = models.CharField(max_length=200)

    def __str__(self):
        return self.text
