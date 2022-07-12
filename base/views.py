from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Classe, Room, Message
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Programmer'},
#     {'id': 2, 'name': 'Python'},
#     {'id': 3, 'name': 'Django'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos!")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Um erro ocorreu!")

    context = {'register': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get(
        'q') != None else ''
    rooms = Room.objects.filter(Q(classe__name__icontains=q) | Q(
        name__icontains=q) | Q(desc__icontains=q))

    classes = Classe.objects.all()
    room_count = rooms.count()
    classes_count = classes.count()

    context = {'rooms': rooms, 'classes': classes,
               'q': q, 'room_count': room_count, 'classes_count': classes_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
