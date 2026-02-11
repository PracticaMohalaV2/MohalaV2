from django.urls import path
from django.contrib.auth.views import LogoutView
from . import logica as views
from .logica import validador_login, seguimiento # <--- Importamos el nuevo archivo

urlpatterns = [
    path('login/', validador_login.login_view, name='login'),
    
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', views.index, name='index'),
    
    path('seguimiento/', seguimiento.panel_seguimiento, name='seguimiento_admin'),
    
    path('autoevaluacion/<int:trabajador_id>/', 
         views.cuestionario_autoevaluacion, 
         name='autoevaluacion_inicio'),
    
    path('autoevaluacion/<int:trabajador_id>/<str:dimension>/', 
         views.cuestionario_autoevaluacion, 
         name='autoevaluacion'),

    path('autoevaluacion/finalizar/<int:trabajador_id>/', 
         views.finalizar_autoevaluacion, 
         name='finalizar_autoevaluacion'),

    path('evaluacion_jefe/<int:evaluador_id>/<int:evaluado_id>/', 
         views.cuestionario_jefatura, 
         name='evaluacion_jefe_inicio'),
    
    path('evaluacion_jefe/<int:evaluador_id>/<int:evaluado_id>/<str:dimension>/', 
         views.cuestionario_jefatura, 
         name='evaluacion_jefe'),

    path('evaluacion_jefe/finalizar/<int:evaluador_id>/<int:evaluado_id>/', 
         views.finalizar_evaluacion_jefe, 
         name='finalizar_evaluacion_jefe'),

    path('resultados/<int:trabajador_id>/<str:tipo_evaluacion>/', 
         views.ver_resultados, 
         name='ver_resultados'),
]