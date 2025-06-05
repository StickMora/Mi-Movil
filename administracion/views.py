from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Productos, User, Reparacion, Ventas, DetalleVenta
from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
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


class VentaListView(LoginRequiredMixin, ListView):
    model = Ventas
    template_name = 'ventas.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(cliente__first_name__icontains=query) |
                Q(cliente__last_name__icontains=query) |
                Q(vendedor__first_name__icontains=query) |
                Q(vendedor__last_name__icontains=query)
            )
        return queryset


class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Ventas
    form_class = VentaForm
    template_name = 'ventas_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        productos = Productos.objects.all()
        if self.request.POST:
            data['detalle_formset'] = DetalleVentaFormSet(self.request.POST, form_kwargs={'productos': productos})
        else:
            data['detalle_formset'] = DetalleVentaFormSet(form_kwargs={'productos': productos})
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if detalle_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.total_venta = 0
            self.object.save()
            detalle_formset.instance = self.object
            detalle_formset.save()

            # Calcular total y actualizar stock
            total_venta = 0
            for detalle in self.object.detalleventa_set.all():
                detalle.precio_unitario = detalle.producto.precio_unitario
                detalle.total_a_pagar = detalle.cantidad * detalle.precio_unitario
                detalle.save()

                detalle.producto.stock_total -= detalle.cantidad
                detalle.producto.save()

                total_venta += detalle.total_a_pagar

            self.object.total_venta = total_venta
            self.object.save()

            return redirect('ventas')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class VentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Ventas
    form_class = VentaForm
    template_name = 'venta_edit_form.html'
    success_url = reverse_lazy('ventas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method in ['POST', 'PUT']:
            context['detalle_formset'] = DetalleVentaFormSet(self.request.POST, instance=self.object)
        else:
            context['detalle_formset'] = DetalleVentaFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        detalle_formset = context['detalle_formset']

        if detalle_formset.is_valid():
            venta = form.save(commit=False)

            # Reponer stock anterior
            for detalle in venta.detalleventa_set.all():
                detalle.producto.stock_total += detalle.cantidad
                detalle.producto.save()

            venta.total_venta = Decimal('0.00')
            venta.save()

            # Guardar detalles nuevos
            detalle_formset.instance = venta
            detalle_formset.save()

            total_venta = Decimal('0.00')

            for detalle in venta.detalleventa_set.all():
                producto = detalle.producto
                cantidad = detalle.cantidad

                # Verificar stock suficiente
                if producto.stock_total < cantidad:
                    detalle_formset.add_error(None, f"Stock insuficiente para {producto.nombre}.")
                    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        html = render_to_string(self.template_name, context, request=self.request)
                        return JsonResponse({'success': False, 'html': html})
                    return self.render_to_response(context)

                detalle.precio_unitario = producto.precio_unitario
                detalle.total_a_pagar = cantidad * producto.precio_unitario
                detalle.save()

                producto.stock_total -= cantidad
                producto.save()

                total_venta += detalle.total_a_pagar

            venta.total_venta = total_venta
            venta.save()
            print(f"DEBUG: Venta actualizada con total {total_venta}")

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            messages.success(self.request, "Venta actualizada correctamente.")
            return super().form_valid(form)

        else:
            print("ERROR: detalle_formset no es válido")
            print(detalle_formset.errors)

        # Formset inválido
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context, request=self.request)
            return JsonResponse({'success': False, 'html': html})

        return self.render_to_response(context)

    def form_invalid(self, form):
        print("ERROR: form_invalid llamado")
        context = self.get_context_data(form=form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context, request=self.request)
            return JsonResponse({'success': False, 'html': html})
        return super().form_invalid(form)


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Ventas
    success_url = reverse_lazy('ventas')

    def delete(self, request, *args, **kwargs):
        venta = self.get_object()

        # Restaurar stock al eliminar la venta
        for detalle in venta.detalleventa_set.all():
            producto = detalle.producto
            producto.stock_total += detalle.cantidad
            producto.save()

        venta.delete()
        messages.success(request, "Venta eliminada correctamente.")
        return super().delete(request, *args, **kwargs)
