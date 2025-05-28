from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Productos, User, Reparacion
from django.db import transaction
from django.db.models import Q
from .forms import RegistroForm, ProductosForm, ClienteForm, ReparacionForm, VentaForm, DetalleVentaFormSet

class HomeRedirectView(RedirectView):
    pattern_name = 'login'


class RegistroView(View):
    form_class = RegistroForm
    template_name = 'registro.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class ProductoListCreateView(LoginRequiredMixin, CreateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos.html'
    success_url = reverse_lazy('producto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        if query:
            context['productos'] = Productos.objects.filter(
                Q(nombre__icontains=query) |
                Q(categoria_producto__nombre__icontains=query) |
                Q(codigo__icontains=query)
            )
        else:
            context['productos'] = Productos.objects.all()
        context['query'] = query
        return context
    

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'editar_producto.html'
    success_url = reverse_lazy('producto')


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Productos
    success_url = reverse_lazy('producto')


class ClienteListCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = ClienteForm
    template_name = 'clientes.html'
    success_url = reverse_lazy('clientes')

    def form_valid(self, form):
        form.instance.tipo_usuario = 'cliente'
        form.instance.set_unusable_password()
        form.instance.is_active = True
        form.instance.is_staff = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        if query:
            clientes = User.objects.filter(
                Q(tipo_usuario='cliente'),
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(username__icontains=query)
            )
        else:
            clientes = User.objects.filter(tipo_usuario='cliente')
        context['clientes'] = clientes
        context['query'] = query
        return context


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ClienteForm
    template_name = 'editar_cliente.html'
    success_url = reverse_lazy('clientes')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('clientes')


class ReparacionListCreateView(LoginRequiredMixin, CreateView):
    model = Reparacion
    form_class = ReparacionForm
    template_name = 'reparaciones.html'
    success_url = reverse_lazy('reparaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        if query:
            reparaciones = Reparacion.objects.filter(
                Q(marca_celular__icontains=query) |
                Q(referencia_celular__icontains=query) |
                Q(estado_reparacion__nombre__icontains=query) |
                Q(cliente__user__first_name__icontains=query) |
                Q(cliente__user__last_name__icontains=query)
            )
        else:
            reparaciones = Reparacion.objects.all()
        context['reparaciones'] = reparaciones
        context['query'] = query
        return context
    

class ReparacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Reparacion
    form_class = ReparacionForm
    template_name = 'editar_reparacion.html'
    success_url = reverse_lazy('reparaciones')


class ReparacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Reparacion
    success_url = reverse_lazy('reparaciones')


class VentaCreateView(View):
    def get(self, request):
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet()
        return render(request, 'ventas.html', {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset
        })

    def post(self, request):
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleVentaFormSet(request.POST)
        if venta_form.is_valid() and detalle_formset.is_valid():
            with transaction.atomic():
                venta = venta_form.save(commit=False)
                venta.total = 0
                venta.save()
                total = 0
                for form in detalle_formset:
                    detalle = form.save(commit=False)
                    detalle.venta = venta
                    detalle.precio_unitario = detalle.producto.precio
                    detalle.precio_total = detalle.precio_unitario * detalle.cantidad
                    total += detalle.precio_total
                    detalle.save()

                    # descontar stock
                    detalle.producto.stock -= detalle.cantidad
                    detalle.producto.save()
                venta.total = total
                venta.save()
                return redirect('ventas')
        return render(request, 'ventas.html', {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset
        })