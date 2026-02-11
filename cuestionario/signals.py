from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Trabajador

@receiver(post_save, sender=Trabajador)
def crear_usuario_automatico(sender, instance, created, **kwargs):
    if created:
        # Si el trabajador es nuevo y no tiene usuario asignado
        if not instance.user:
            # 1. Creamos el usuario base
            nuevo_usuario = User.objects.create_user(
                username=instance.email,
                email=instance.email,
                password='Mohala2026'
            )
            
            # 2. Forzamos la grabación de nombres y apellidos
            nuevo_usuario.first_name = instance.nombre
            nuevo_usuario.last_name = f"{instance.apellido_paterno} {instance.apellido_materno}"
            nuevo_usuario.is_staff = False
            nuevo_usuario.save()

            # 3. Vinculamos al trabajador con el usuario recién creado
            Trabajador.objects.filter(id=instance.id).update(user=nuevo_usuario)
            
    else:
        if instance.user:
            user = instance.user
            user.first_name = instance.nombre
            user.last_name = f"{instance.apellido_paterno} {instance.apellido_materno}"
            # Aseguramos que siempre el email sea el username
            user.username = instance.email
            user.email = instance.email
            user.save()