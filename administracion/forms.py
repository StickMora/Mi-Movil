# administracion/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'tipo_usuario', 'telefono', 'password1', 'password2']


class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria_producto': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }