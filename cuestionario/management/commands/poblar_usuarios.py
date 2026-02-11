from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cuestionario.models import Trabajador

class Command(BaseCommand):
    help = 'Crea y vincula usuarios de Django para trabajadores'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando vinculación de usuarios...')
        trabajadores_sin_user = Trabajador.objects.filter(user__isnull=True)
        
        contador = 0
        for t in trabajadores_sin_user:
            user, created = User.objects.get_or_create(
                username=t.email,
                defaults={
                    'email': t.email, 
                    'first_name': t.nombre,
                    'last_name': f"{t.apellido_paterno} {t.apellido_materno}",
                    'is_staff': False
                }
            )
            
            # Sincronizamos nombres y quitamos staff
            user.first_name = t.nombre
            user.last_name = f"{t.apellido_paterno} {t.apellido_materno}"
            user.set_password('Mohala2026')
            user.is_staff = False 
            user.save()
            
            t.user = user
            t.save()
            
            # Mensaje limpio para la consola
            self.stdout.write(self.style.SUCCESS(f"✅ Usuario procesado: {t.email}"))
            contador += 1

        self.stdout.write(self.style.SUCCESS(f'--- Proceso finalizado. {contador} usuarios listos ---'))