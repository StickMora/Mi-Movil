# administracion/forms.py
from django import forms
from django.forms import inlineformset_factory
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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'telefono']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'motivo_ingreso': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado_reparacion': forms.Select(attrs={'class': 'form-control'}),
            'marca_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'abono': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.select_related('user')


class VentaForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

DetalleVentaFormSet = inlineformset_factory(
    Ventas, DetalleVenta,
    fields=('producto', 'cantidad', 'precio_unitario', 'precio_total'),
    widgets={
        'producto': forms.Select(attrs={'class': 'form-select producto-select'}),
        'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': '1'}),
        'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-unitario', 'readonly': 'readonly'}),
        'precio_total': forms.NumberInput(attrs={'class': 'form-control precio_total', 'readonly': 'readonly'}),
    },
    extra=1,
    can_delete=True
)