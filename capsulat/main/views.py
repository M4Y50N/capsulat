from django.shortcuts import render
from django.http import HttpResponse
from .models import AlgoPFazer, Item
# Create your views here.


def index(response, id):
    ls = AlgoPFazer.objects.get(id=id)
    return render(response, "main/list.html", {"ls": ls})


def home(response):
    return render(response, "main/home.html", {"name": "teste"})
