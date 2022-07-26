from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Classe, Room, Message
from .forms import RoomForm

from datetime import datetime
from pytz import timezone

# Criptografar string
from simplecrypt import encrypt, decrypt

# m = 'mayson'
# k = Fernet.generate_key()
# fernet = Fernet(k)

# l = fernet.encrypt(m.encode())

# print(k)

def timesince(dt, default="agora"):
    now = datetime.now()
    diff = now - dt
    periods = (
        (diff.days // 365, "ano", "anos"),
        (diff.days // 30, "mês", "meses"),
        (diff.days // 7, "semana", "semanas"),
        (diff.days, "dia", "dias"),
        (diff.seconds // 3600, "hora", "horas"),
        (diff.seconds // 60, "minuto", "minutos"),
        (diff.seconds - 30, "segundo", "segundos"),
    )
    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s atrás" % (period, singular if period == 1 else plural)
    return default

# Função para calcular a hora que foi criado a Room/Classe/Message
def howLongAgo(datas):
    for data in datas:
        wasCreated = data.created
        fuso_horario = timezone('America/Sao_Paulo')

        data_e_hora_sao_paulo = wasCreated.astimezone(fuso_horario)
        wasCreated_format = data_e_hora_sao_paulo.strftime(
            "%d/%m/%Y %H:%M")

        data_created, hour_created = wasCreated_format.split(' ')

        data_created = data_created + " " + hour_created

        # dia mes ano
        d = int(data_created.split('/')[0])
        m = int(data_created.split('/')[1])
        y = int(data_created.split('/')[2].split(' ')[0])

        # hora minuto
        h = int(hour_created.split(':')[0])
        mi = int(hour_created.split(':')[1])

        data.created_in = timesince(datetime(y, m, d, h, mi, 0))
        data.save()


#função para criptografar
@login_required(login_url='login')
def nowCrypDecryp(request, pk):
    room = Room.objects.get(id=pk)
    key = room.crypt_key
    
    if request.method == 'POST':
        input_key = request.POST.get('cryp_key')
        act = request.POST.get('act')
        if input_key == room.crypt_key:
            if act == 'cryp':
                for msg in room.message_set.all():
                    if type(msg.body) != bytes:
                        c = encrypt(key, msg.body)
                        msg.body = c
                        msg.save()
            else:
                for msg in room.message_set.all():
                    c = decrypt(key, eval(msg.body)).decode('utf-8')
                    msg.body = c
                    msg.save()
        # else:
        #     messages.error(request, 'Chave inexistente')

    return render(request, 'base/cryp_key.html', {'obj': room})


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
        name__icontains=q) | Q(desc__icontains=q)).order_by('-created')

    howLongAgo(rooms)

    classes = Classe.objects.all()
    room_count = rooms.count()

    room_messages = Message.objects.filter(
        Q(room__classe__name__icontains=q) | Q(
            room__name__icontains=q)).order_by('-created')

    howLongAgo(room_messages)

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

    howLongAgo(room_messages)

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
        crypt_key = request.POST.get('crypt_key')
        classe, created = Classe.objects.get_or_create(name=classe_name)

        Room.objects.create(
            host=request.user,
            classe=classe,
            room_join=request.POST.get('room_join'),
            crypt_key=crypt_key,
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
        room.room_join=request.POST.get('room_join')
        room.crypt_key = request.POST.get('crypt_key')
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
def joinRoom(request, pk):
    room = Room.objects.get(id=pk)
    participantes = room.participants.all()

    for p in participantes:
        if p == request.user:
            room.participants.add(request.user)
            return redirect('room', pk)
    
    if request.user == room.host:
        return redirect('room', pk)


    if request.method == 'POST':
        if room.room_join == request.POST.get('room_join'):
            room.participants.add(request.user)
            return redirect('room', pk)
        else:
            return redirect('home')
    return render(request, 'base/join_room.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room_id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)
