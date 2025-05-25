# administracion/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Categoria, Estado, Ventas, Productos, DetalleVenta

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
        ('Datos cliente', {
            'fields': ('telefono', 'motivo_ingreso', 'estado_celular', 'tipo_celular', 'datos_celular', 'fecha_ingreso', 'fecha_salida')
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Categoria)
admin.site.register(Estado)
admin.site.register(Ventas)
admin.site.register(Productos)
admin.site.register(DetalleVenta)
