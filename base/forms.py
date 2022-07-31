from django.forms import ModelForm
from django.forms import DateInput
from .models import Room, User




class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'date_control_initial': DateInput()
        }

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']