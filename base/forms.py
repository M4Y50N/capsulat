from django.forms import ModelForm
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def __init__(self,*args,**kwargs):
        super(UserRegisterForm,self).__init__(*args,**kwargs)

        self.fields['name'].label = 'Nome'

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
        fields = ['avatar','name', 'username', 'email', 'bio']
