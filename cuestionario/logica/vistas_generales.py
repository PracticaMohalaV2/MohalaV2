from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura

@login_required
def index(request):
    # 1. VALIDACIÓN PARA ADMINISTRADOR
    if request.user.is_superuser:
        context = {
            'es_admin_sistema': True,
            'nombre_usuario': request.user.username,
            'trabajador': None,
            'es_jefe': False,
            'equipo': [],
            'ya_hizo_autoevaluacion': False,
        }
        return render(request, 'cuestionario/index.html', context)

    # 2. FLUJO NORMAL PARA TRABAJADORES
    trabajador = get_object_or_404(Trabajador, user=request.user)
    
    autoeval_completada = Autoevaluacion.objects.filter(
        trabajador=trabajador, 
        estado_finalizacion=True
    ).exists()
    
    equipo = trabajador.subordinados.all()
    
    for sub in equipo:
        sub.autoevaluacion_terminada = Autoevaluacion.objects.filter(
            trabajador=sub, 
            estado_finalizacion=True
        ).exists()
        
        sub.ya_evaluado = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=sub,
            estado_finalizacion=True
        ).exists()

    context = {
        'trabajador': trabajador,
        'es_jefe': trabajador.subordinados.exists(),
        'equipo': equipo,
        'ya_hizo_autoevaluacion': autoeval_completada,
        'es_admin_sistema': False,
    }
    return render(request, 'cuestionario/index.html', context)

@login_required
def ver_resultados(request, trabajador_id, tipo_evaluacion):
    # (El resto de la función se mantiene igual)
    trabajador_autenticado = get_object_or_404(Trabajador, user=request.user)
    trabajador_a_ver = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    dimension_filtro = request.GET.get('dimension')

    if tipo_evaluacion == 'auto':
        respuestas = Autoevaluacion.objects.filter(trabajador=trabajador_a_ver)
        visor_id = trabajador_a_ver.id_trabajador
    else:
        evaluador_id = request.GET.get('evaluador_id')
        respuestas = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador_a_ver, evaluador_id=evaluador_id)
        visor_id = evaluador_id

    respuestas = respuestas.select_related('codigo_excel__competencia__dimension')

    if dimension_filtro:
        respuestas = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension_filtro)

    dimensiones_data = {}
    dimensiones_nombres = respuestas.values_list('codigo_excel__competencia__dimension__nombre_dimension', flat=True).distinct()
    
    for dim in dimensiones_nombres:
        dimensiones_data[dim] = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension=dim)

    context = {
        'trabajador': trabajador_a_ver,
        'dimensiones': dimensiones_data,
        'comentario_final': respuestas.first().comentario if respuestas.exists() else "",
        'fecha_cierre': respuestas.first().momento_evaluacion if respuestas.exists() else None,
        'visor_id': visor_id,
        'tipo_evaluacion': tipo_evaluacion
    }
    return render(request, 'cuestionario/ver_resultados.html', context)