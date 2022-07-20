from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Classe, Room, Message
from .forms import RoomForm


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

    room_messages = Message.objects.filter(
        Q(room__classe__name__icontains=q) | Q(
            room__name__icontains=q)).order_by('-created')

    recent_activity = room_messages[:6]

    context = {'rooms': rooms, 'classes': classes,
               'q': q, 'room_count': room_count, 'room_messages': room_messages,
               'recent_activity': recent_activity}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, pk):

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participantes = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participantes': participantes}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    room_messages = user.message_set.all().order_by('-created')

    classes = Classe.objects.all()

    recent_activity = room_messages[:6]

    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'classes': classes, 'recent_activity': recent_activity}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    classes = Classe.objects.all()
    if request.method == 'POST':
        classe_name = request.POST.get('classe')
        classe, created = Classe.objects.get_or_create(name=classe_name)

        Room.objects.create(
            host=request.user,
            classe=classe,
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
        )

        return redirect('home')

    context = {'form': form, 'classes': classes}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    classes = Classe.objects.all()
    if request.method == 'POST':
        classe_name = request.POST.get('classe')
        classe, created = Classe.objects.get_or_create(name=classe_name)
        room.name = request.POST.get('name')
        room.classe = classe
        room.desc = request.POST.get('desc')
        room.save()
        return redirect('home')

    context = {'form': form, 'room': room, 'classes': classes}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room_id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)
