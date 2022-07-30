from django.forms import ModelForm
from django import forms
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class DateControl(forms.Form):
    date_field = forms.DateField()