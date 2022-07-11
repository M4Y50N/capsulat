from django.contrib import admin

from .models import Classe, Message, Room

admin.site.register(Classe)
admin.site.register(Room)
admin.site.register(Message)
