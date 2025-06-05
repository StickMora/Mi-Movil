from django.urls import path
from .views import (
    HomeRedirectView, RegistroView, 
    ProductoListCreateView, ProductoUpdateView, ProductoDeleteView,  
    ClienteListCreateView, ClienteUpdateView, ClienteDeleteView, 
    ReparacionListCreateView, ReparacionUpdateView, ReparacionDeleteView, 
    VentaListView, VentaCreateView, VentaUpdateView, VentaDeleteView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='home'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('clientes/', ClienteListCreateView.as_view(), name='clientes'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),

    path('producto/', ProductoListCreateView.as_view(), name='producto'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),

    path('reparaciones/', ReparacionListCreateView.as_view(), name='reparaciones'),
    path('reparacion/editar/<int:pk>/', ReparacionUpdateView.as_view(), name='editar_reparacion'),
    path('reparacion/eliminar/<int:pk>/', ReparacionDeleteView.as_view(), name='eliminar_reparacion'),

    path('ventas/', VentaListView.as_view(), name='ventas'),
    path('ventas/nueva/', VentaCreateView.as_view(), name='crear_venta'),
    path('ventas/editar/<int:pk>/', VentaUpdateView.as_view(), name='editar_venta'),
    path('ventas/eliminar/<int:pk>/', VentaDeleteView.as_view(), name='eliminar_venta'),
]
