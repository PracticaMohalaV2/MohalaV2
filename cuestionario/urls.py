from django.urls import path
from django.contrib.auth.views import LogoutView
from . import logica as views
from .logica import validador_login, seguimiento, detalle_seguimiento, reporte_pdf, reporte_excel, gemini_admin, reporte_global, manejo_archivos

urlpatterns = [
    path('login/', validador_login.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.index, name='index'),
    
    path('seguimiento/', seguimiento.panel_seguimiento, name='seguimiento_admin'),
    
    path('seguimiento/detalle/<int:trabajador_id>/', 
         detalle_seguimiento.detalle_seguimiento, 
         name='detalle_seguimiento'),
    
    path('seguimiento/detalle/<int:trabajador_id>/pdf/', 
         reporte_pdf.generar_pdf_detalle, 
         name='generar_pdf_detalle'),
    
    path('seguimiento/detalle/<int:trabajador_id>/excel/', 
         reporte_excel.generar_excel_detalle, 
         name='generar_excel_detalle'),
     
    path('seguimiento/reporte-global/', 
         reporte_global.generar_reporte_global_pdf, 
         name='generar_reporte_global_pdf'),
    
    path('seguimiento/ver-reporte-global/<int:reporte_id>/', 
         reporte_global.ver_reporte_global_pdf, 
         name='ver_reporte_global_pdf'),

     path('biblioteca/ver-archivo/<int:biblioteca_id>/', 
          manejo_archivos.ver_archivo_biblioteca, 
          name='ver_archivo_biblioteca'),
    
    # RUTAS GEMINI
    path('gemini/', gemini_admin.panel_gemini, name='panel_gemini'),
    path('gemini/editar-prompt/', gemini_admin.editar_prompt, name='editar_prompt'),
    path('gemini/generar/<int:prompt_id>/', gemini_admin.generar_informe_gemini, name='generar_informe_gemini'),
    path('gemini/listar-modelos/', gemini_admin.listar_modelos, name='listar_modelos'),
    path('gemini/ver-informe/<int:prompt_id>/', gemini_admin.ver_informe_gemini, name='ver_informe_gemini'),
    
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