from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura, ResultadoConsolidado

@login_required
def detalle_resultado(request, trabajador_id):
    if not request.user.is_superuser:
        return redirect('index')
    
    trabajador = Trabajador.objects.get(id_trabajador=trabajador_id)
    
    resultados = ResultadoConsolidado.objects.filter(
        trabajador=trabajador
    ).select_related('codigo_excel', 'competencia', 'dimension').order_by('codigo_excel__codigo_excel')
    
    # Calcular diferencia promedio total
    diff_promedio = resultados.aggregate(Avg('diferencia'))['diferencia__avg']
    
    # Obtener timestamps de finalización
    auto = Autoevaluacion.objects.filter(trabajador=trabajador, estado_finalizacion=True).first()
    jefe = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador, estado_finalizacion=True).first()
    
    # Usar momento_evaluacion en lugar de fecha_finalizacion
    timestamp_auto = auto.momento_evaluacion if auto else None
    timestamp_jefe = jefe.momento_evaluacion if jefe else None
    
    context = {
        'trabajador': trabajador,
        'resultados': resultados,
        'diff_promedio': diff_promedio,
        'timestamp_auto': timestamp_auto,
        'timestamp_jefe': timestamp_jefe,
    }
    
    return render(request, 'cuestionario/detalle_seguimiento.html', context)