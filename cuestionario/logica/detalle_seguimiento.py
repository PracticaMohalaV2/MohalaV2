from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura, ResultadoConsolidado

@login_required
def detalle_seguimiento(request, trabajador_id):
    if not request.user.is_superuser:
        return redirect('index')
    
    try:
        trabajador = Trabajador.objects.select_related('cargo', 'nivel_jerarquico', 'id_jefe_directo').get(id_trabajador=trabajador_id)
    except Trabajador.DoesNotExist:
        return redirect('seguimiento_admin')
    
    resultados = ResultadoConsolidado.objects.filter(
        trabajador=trabajador
    ).select_related('codigo_excel', 'competencia', 'dimension').order_by('codigo_excel__id_textos_evaluacion')
    
    # Separar resultados por dimensión
    resultados_organizacionales = resultados.filter(dimension__nombre_dimension__icontains='Organizacional')
    resultados_funcionales = resultados.filter(dimension__nombre_dimension__icontains='Funcional')
    
    # Calcular promedios por dimensión
    diff_promedio_org = resultados_organizacionales.aggregate(Avg('diferencia'))['diferencia__avg']
    diff_promedio_func = resultados_funcionales.aggregate(Avg('diferencia'))['diferencia__avg']
    diff_promedio_total = resultados.aggregate(Avg('diferencia'))['diferencia__avg']
    
    auto = Autoevaluacion.objects.filter(trabajador=trabajador, estado_finalizacion=True).first()
    jefe = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador, estado_finalizacion=True).first()
    
    timestamp_auto = auto.momento_evaluacion if auto else None
    timestamp_jefe = jefe.momento_evaluacion if jefe else None
    
    context = {
        'trabajador': trabajador,
        'resultados_organizacionales': resultados_organizacionales,
        'resultados_funcionales': resultados_funcionales,
        'diff_promedio_org': diff_promedio_org,
        'diff_promedio_func': diff_promedio_func,
        'diff_promedio_total': diff_promedio_total,
        'timestamp_auto': timestamp_auto,
        'timestamp_jefe': timestamp_jefe,
    }
    
    return render(request, 'cuestionario/detalle_seguimiento.html', context)