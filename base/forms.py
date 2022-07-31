from sqlite3 import Date
from django.forms import ModelForm
from django.forms import DateInput
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'date_control_initial': DateInput()
        }
