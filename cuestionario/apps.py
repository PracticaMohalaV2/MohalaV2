from django.apps import AppConfig

class CuestionarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cuestionario'

    def ready(self):
        # Esto importa las señales cuando Django arranca
        import cuestionario.signals