from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
    ]

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de usuario")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Apellidos")
    telefono = models.IntegerField(verbose_name="Número de Teléfono")
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de usuario")

    is_staff = models.BooleanField(default=False, verbose_name="Es administrador")
    is_active = models.BooleanField(default=True, verbose_name="Está activo")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Fecha de registro")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email
 

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, verbose_name="Usuario")   

    def __str__(self):
        return self.user.get_full_name()

    
class Categoria(models.Model):
    nombre = models.CharField(max_length=45, verbose_name="Nombre")

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=45, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre


class TipoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de pago")

    def __str__(self):
        return self.nombre



class Ventas(models.Model):
    fecha_venta = models.DateField(null=True, blank=True, verbose_name="Fecha de venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="ventas", verbose_name="Cliente")
    estado_venta = models.CharField(max_length=45, verbose_name="Estado de la venta")
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="ventas_registradas", verbose_name="Empleado responsable")

    def __str__(self):
        return f"Venta {self.id} - {self.estado_venta}"


class Productos(models.Model):
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name="Imagen del producto")
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    codigo = models.CharField(max_length=45, verbose_name="Código")
    stock_total = models.IntegerField(verbose_name="Stock total")
    stock_min = models.IntegerField(verbose_name="Stock mínimo")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoría")

    def __str__(self):
        return self.nombre


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, verbose_name="Venta")
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio total")
    iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IVA")
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Total a pagar")
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de pago")
    fecha_venta = models.DateTimeField(verbose_name="Fecha de venta")

    def __str__(self):
        return f"DetalleVenta {self.id} - {self.id_producto.nombre}"
    
    
class Reparacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reparaciones')
    motivo_ingreso = models.CharField(max_length=100, blank=True, null=True, verbose_name="Motivo de ingreso")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    estado_reparacion = models.ForeignKey(Estado, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Estado de la Reparación")
    marca_celular = models.CharField(max_length=45, blank=True, null=True, verbose_name="Marca del celular")
    referencia_celular = models.CharField(max_length=45, blank=True, null=True, verbose_name="Referencia del celular")
    precio_total = models.IntegerField(blank=True, null=True, verbose_name="Precio total")
    abono = models.IntegerField(blank=True, null=True, verbose_name="Abono")
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de pago")
    fecha_ingreso = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de ingreso")
    fecha_salida = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de salida")

    def saldo_pendiente(self):
        return (self.precio_total or 0) - (self.abono or 0)

    def __str__(self):
        return f"Reparación de {self.marca_celular} - {self.referencia_celular} ({self.cliente})"