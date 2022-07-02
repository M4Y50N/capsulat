from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Sala, Participante
from .forms import CreateNewList
# Create your views here.


def index(response, id):
    ls = Sala.objects.get(id=id)

    if response.method == "POST":
        if response.POST.get('save'):
            print(response.POST)
            for item in ls.participante_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    pass
                else:
                    pass
                item.save()
        elif response.POST.get('newItem'):
            txt = response.POST.get('new')

            ls.participante_set.create(text=txt)

    return render(response, "main/turma.html", {"ls": ls})


def home(response):
    return render(response, "main/home.html", {"name": "teste"})


def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = Sala(name=n)
            t.save()
            response.user.sala.add(t)

        return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})


def view(response):
    allF = Sala.objects.all()
    return render(response, "main/view.html", {"list": allF})
