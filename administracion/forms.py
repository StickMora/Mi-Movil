# administracion/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'tipo_usuario', 'telefono', 'password1', 'password2']
