from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Classe, Room, Message, User
from .forms import RoomForm, UserForm, UserRegisterForm

import datetime as dtTime
from datetime import date, datetime
from pytz import timezone

# Criptografar string
from simplecrypt import encrypt, decrypt


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
        (diff.seconds, "segundo", "segundos"),
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
            "%d/%m/%Y %H:%M:%S")

        data_created, hour_created = wasCreated_format.split(' ')

        data_created = data_created + " " + hour_created

        # dia mes ano
        d = int(data_created.split('/')[0])
        m = int(data_created.split('/')[1])
        y = int(data_created.split('/')[2].split(' ')[0])

        # hora minuto
        h = int(hour_created.split(':')[0])
        mi = int(hour_created.split(':')[1])
        s = int(hour_created.split(':')[2])

        data.created_in = timesince(datetime(y, m, d, h, mi, s))
        data.save()


#função para criptografar
def nowCryp(request, pk):
    room = Room.objects.get(id=pk)
    key = room.crypt_key
    
    for msg in room.message_set.all():
        try:
            if type(eval(msg.body)) != bytes:
                c = encrypt(key, msg.body)
                msg.body = c
                msg.save()
        except:
            if type(msg.body) != bytes:
                c = encrypt(key, msg.body)
                msg.body = c
                msg.save()
    
    return 'crypted'

def nowDecryp(request, pk):
    room = Room.objects.get(id=pk)
    key = room.crypt_key

    for msg in room.message_set.all():
        try:
            if type(eval(msg.body)) == bytes:
                c = decrypt(key, eval(msg.body)).decode('utf-8')
                msg.body = c
                msg.save()
        except:
            if type(msg.body) == bytes:
                c = decrypt(key, eval(msg.body)).decode('utf-8')
                msg.body = c
                msg.save()        

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, email=email, password=password)

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
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
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
    cryp_decryp = ''
    
    if room.date_control_end == datetime.today().date():
        print('é agr')
        nowDecryp(request, pk)
    
    elif room.date_control_initial == datetime.today().date():
        cryp_decryp = nowCryp(request, pk)
            

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
               'participantes': participantes, 'cryp_decryp': cryp_decryp}
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
    return render(request, 'base/user_posts.html', context)

@login_required(login_url='login')
def userConfig(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/profile.html', {'form': form})

def formatDate(date_p, request):
    if len(date_p.split('/')) == 3:
        new_str = []
        for i in date_p.split('/'):
            new_str.append(i)
        return '-'.join(list(reversed(new_str)))
    else:
        return messages.error(request, "Data invalida")

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
 
    classes = Classe.objects.all()
    if request.method == 'POST':
        classe_name = request.POST.get('classe')
        crypt_key = request.POST.get('crypt_key')
        date_control_initial = formatDate(request.POST.get('date_control_initial'), request)
        date_control_end = formatDate(request.POST.get('date_control_end'), request)
        classe, created = Classe.objects.get_or_create(name=classe_name)

        Room.objects.create(
            host=request.user,
            classe=classe,
            room_join=request.POST.get('room_join'),
            crypt_key=crypt_key,
            date_control_initial = date_control_initial,
            date_control_end = date_control_end,
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
        date_control_initial = formatDate(request.POST.get('date_control_initial'), request)
        date_control_end = formatDate(request.POST.get('date_control_end'), request)

        room.name = request.POST.get('name')
        room.classe = classe
        room.room_join=request.POST.get('room_join')
        room.date_control_initial = date_control_initial
        room.date_control_end = date_control_end
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
            return redirect('room', pk=room.id)
    
    if request.user == room.host:
        return redirect('room', pk=room.id)


    if request.method == 'POST':
        if room.room_join == request.POST.get('room_join'):
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
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
