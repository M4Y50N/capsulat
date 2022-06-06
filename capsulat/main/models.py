from statistics import mode
from django.db import models

# Create your models here.


class AlgoPFazer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    AlgoPFazer = models.ForeignKey(AlgoPFazer, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
