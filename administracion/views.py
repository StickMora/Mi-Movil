from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Productos
from .forms import RegistroForm, ProductosForm

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
        context['productos'] = Productos.objects.all()
        return context

    

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'editar_producto_form.html'
    success_url = reverse_lazy('producto')


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Productos
    success_url = reverse_lazy('producto')


class VentasView(LoginRequiredMixin, TemplateView):
    template_name = 'ventas.html'


class ClientesView(LoginRequiredMixin, TemplateView):
    template_name = 'clientes.html'