# Generated by Django 4.2.21 on 2025-05-25 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Nombre de usuario')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Apellidos')),
                ('tipo_usuario', models.CharField(choices=[('cliente', 'Cliente'), ('empleado', 'Empleado')], max_length=10, verbose_name='Tipo de usuario')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Es administrador')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está activo')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de registro')),
                ('telefono', models.CharField(blank=True, max_length=45, null=True, verbose_name='Teléfono')),
                ('motivo_ingreso', models.CharField(blank=True, max_length=45, null=True, verbose_name='Motivo de ingreso')),
                ('tipo_celular', models.CharField(blank=True, max_length=45, null=True, verbose_name='Tipo de celular')),
                ('datos_celular', models.CharField(blank=True, max_length=45, null=True, verbose_name='Datos del celular')),
                ('fecha_ingreso', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de ingreso')),
                ('fecha_salida', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de salida')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=45, null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateField(blank=True, null=True, verbose_name='Fecha de venta')),
                ('estado_venta', models.CharField(max_length=45, verbose_name='Estado de la venta')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas', to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('id_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas_registradas', to=settings.AUTH_USER_MODEL, verbose_name='Usuario responsable')),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=45, verbose_name='Descripción')),
                ('stock_total', models.IntegerField(verbose_name='Stock total')),
                ('stock_min', models.IntegerField(verbose_name='Stock mínimo')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio unitario')),
                ('categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.categoria', verbose_name='Categoría')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio unitario')),
                ('precio_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio total')),
                ('iva', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IVA')),
                ('total_Apagar', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total a pagar')),
                ('fecha_venta', models.DateTimeField(verbose_name='Fecha de venta')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.productos', verbose_name='Producto')),
                ('id_ventas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.ventas', verbose_name='Venta')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='estado_celular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='administracion.estado', verbose_name='Estado del celular'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
