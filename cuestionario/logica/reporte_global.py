from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from cuestionario.models import Trabajador, ResultadoConsolidado, Autoevaluacion, EvaluacionJefatura, ReporteGlobal
from weasyprint import HTML
from io import BytesIO
from datetime import datetime


@login_required
def generar_reporte_global_pdf(request):
    """Generar un PDF con todos los reportes individuales concatenados usando HTML"""
    if not request.user.is_superuser:
        return redirect('index')
    
    # Obtener todos los trabajadores con evaluaciones completas
    trabajadores_data = []
    
    trabajadores = Trabajador.objects.filter(
        resultados_consolidados__isnull=False
    ).select_related(
        'cargo', 
        'nivel_jerarquico', 
        'id_jefe_directo'
    ).distinct().order_by('apellido_paterno', 'nombre')
    
    if not trabajadores.exists():
        return HttpResponse("No hay trabajadores con evaluaciones completadas", status=404)
    
    # Recopilar datos de cada trabajador
    for trabajador in trabajadores:
        resultados = ResultadoConsolidado.objects.filter(
            trabajador=trabajador
        ).select_related(
            'dimension',
            'competencia',
            'codigo_excel'
        ).order_by('dimension__nombre_dimension', 'codigo_excel__codigo_excel')
        
        if not resultados.exists():
            continue
        
        # Obtener fechas de finalización
        auto = Autoevaluacion.objects.filter(
            trabajador=trabajador, 
            estado_finalizacion=True
        ).order_by('-momento_evaluacion').first()
        
        jefe = EvaluacionJefatura.objects.filter(
            trabajador_evaluado=trabajador,
            estado_finalizacion=True
        ).order_by('-momento_evaluacion').first()
        
        # Separar por dimensiones
        resultados_organizacionales = resultados.filter(dimension__nombre_dimension__icontains='Organizacional')
        resultados_funcionales = resultados.filter(dimension__nombre_dimension__icontains='Funcional')
        
        trabajadores_data.append({
            'trabajador': trabajador,
            'timestamp_auto': auto.momento_evaluacion if auto else None,
            'timestamp_jefe': jefe.momento_evaluacion if jefe else None,
            'resultados_organizacionales': resultados_organizacionales,
            'resultados_funcionales': resultados_funcionales
        })
    
    # Renderizar el template HTML
    context = {
        'trabajadores_data': trabajadores_data,
        'total_trabajadores': len(trabajadores_data),
        'fecha_generacion': datetime.now()
    }
    
    html_string = render_to_string('cuestionario/reporte_global_pdf.html', context)
    
    # Convertir HTML a PDF
    html = HTML(string=html_string)
    pdf_bytes = html.write_pdf()
    
    # Guardar en BD
    reporte_global = ReporteGlobal.objects.create(
        contenido_pdf=pdf_bytes,
        total_trabajadores=len(trabajadores_data),
        periodo=2026
    )
    
    # Devolver PDF al navegador
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_global_{reporte_global.id_reporte_global}.pdf"'
    
    return response