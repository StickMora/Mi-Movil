# administracion/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import BaseInlineFormSet
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
        fields = ['cliente', 'tipo_pago', 'fecha_venta']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'fecha_venta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ProductoSelectWithPrecio(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        try:
            pk = getattr(value, 'value', value)
            if pk and hasattr(self.choices, 'queryset'):
                producto_obj = self.choices.queryset.filter(pk=pk).first()
                if producto_obj:
                    option['attrs']['data-precio'] = str(producto_obj.precio_unitario)
                else:
                    option['attrs']['data-precio'] = '0'
        except Exception as e:
            print("Error obteniendo el producto:", e)
            option['attrs']['data-precio'] = '0'

        return option


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': ProductoSelectWithPrecio(attrs={'class': 'form-select producto-select'}),
        }

    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos', None)
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Productos.objects.all()
        self.fields['producto'].widget.attrs.update({'class': 'form-select producto-select'})


        if productos is not None:
            self.fields['producto'].queryset = productos
            self.fields['producto'].widget.choices.queryset = productos

        self.fields['cantidad'].widget.attrs.update({
            'class': 'form-control cantidad-input',
            'min': 1,
            'value': 1
        })


class BaseDetalleVentaFormSet(BaseInlineFormSet):
    """
    Formset base para pasar productos desde la vista al formset.
    """
    def __init__(self, *args, **kwargs):
        self.form_kwargs = kwargs.pop('form_kwargs', {})
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs.update(self.form_kwargs)
        return super()._construct_form(i, **kwargs)


DetalleVentaFormSet = inlineformset_factory(
    Ventas,
    DetalleVenta,
    form=DetalleVentaForm,
    formset=BaseDetalleVentaFormSet,
    extra=1,
    can_delete=True
)
