from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Cliente 

@receiver(post_save, sender=User)
def crear_cliente_automaticamente(sender, instance, created, **kwargs):
    if created and instance.tipo_usuario == 'cliente':
        Cliente.objects.create(user=instance)
