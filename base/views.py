from multiprocessing import context
from django.shortcuts import render


rooms = [
    {'id': 1, 'name': 'programmer'},
    {'id': 2, 'name': 'Python'},
    {'id': 3, 'name': 'Django'},
]


def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request):
    return render(request, 'room.html')
