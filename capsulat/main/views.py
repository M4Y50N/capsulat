from django.shortcuts import render
from django.http import HttpResponse
from .models import AlgoPFazer, Item
# Create your views here.


def index(response, id):
    ls = AlgoPFazer.objects.get(id=id)
    return HttpResponse(ls.name)
