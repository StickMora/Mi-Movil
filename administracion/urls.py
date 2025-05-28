from django.urls import path
from .views import (
    HomeRedirectView, RegistroView, VentasView, ClientesView,
    # ProductoListView, ProductoCreateView, 
    ProductoUpdateView, ProductoDeleteView, ProductoListCreateView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='home'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('ventas/', VentasView.as_view(), name='ventas'),
    path('clientes/', ClientesView.as_view(), name='clientes'),

    path('producto/', ProductoListCreateView.as_view(), name='producto'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
]
