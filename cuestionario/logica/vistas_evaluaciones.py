from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from cuestionario.models import (
    Trabajador, TextosEvaluacion, Autoevaluacion, 
    EvaluacionJefatura, Escala, DescripcionRespuesta
)
from django.db import transaction
from .calculos import generar_consolidado 

# =========================
# LÓGICA AUTOEVALUACIÓN
# =========================
def cuestionario_autoevaluacion(request, trabajador_id, dimension=None):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    if not dimension:
        respuestas = Autoevaluacion.objects.filter(trabajador=trabajador)
        ya_finalizado = respuestas.filter(estado_finalizacion=True).exists()
        
        total_preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico).count()
        total_respuestas = respuestas.count()
        
        listo_para_enviar = (total_respuestas >= total_preguntas) and not ya_finalizado
        
        hecho_org = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional").exists()
        hecho_fun = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional").exists()
        
        return render(request, 'cuestionario/autoevaluacion_seleccion.html', {
            'trabajador': trabajador,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun,
            'listo_para_enviar': listo_para_enviar,
            'ya_finalizado': ya_finalizado
        })

    ya_respondido = Autoevaluacion.objects.filter(
        trabajador=trabajador,
        codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension
    ).exists()

    if ya_respondido:
        return redirect('autoevaluacion_inicio', trabajador_id=trabajador.id_trabajador)

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('id_textos_evaluacion')

    descripciones_qs = DescripcionRespuesta.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico
    ).select_related('escala')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
                    obj_escala = Escala.objects.get(id_escala=int(puntaje_valor))
                    
                    Autoevaluacion.objects.update_or_create(
                        trabajador=trabajador,
                        codigo_excel=pregunta,
                        defaults={
                            'puntaje': puntaje_valor,
                            'escala': obj_escala,
                            'fecha_evaluacion': timezone.now().date(),
                            'momento_evaluacion': timezone.now(),
                            'comentario': request.POST.get('comentario', ''),
                            'estado_finalizacion': False,
                            'nivel_jerarquico': pregunta.nivel_jerarquico
                        }
                    )
        return redirect('autoevaluacion_inicio', trabajador_id=trabajador.id_trabajador)

    context = {
        'trabajador': trabajador, 
        'preguntas': preguntas_qs, 
        'dimension': dimension,
        'descripciones': descripciones_qs
    }
    return render(request, 'cuestionario/autoevaluacion.html', context)

def finalizar_autoevaluacion(request, trabajador_id):
    if request.method == "POST":
        Autoevaluacion.objects.filter(trabajador_id=trabajador_id).update(estado_finalizacion=True)
        
        trabajador = Trabajador.objects.get(id_trabajador=trabajador_id)
        if trabajador.id_jefe_directo is None:
            generar_consolidado(trabajador)
            
    return redirect('autoevaluacion_inicio', trabajador_id=trabajador_id)

# =========================
# LÓGICA EVALUACIÓN JEFATURA
# =========================
def cuestionario_jefatura(request, evaluador_id, evaluado_id, dimension=None):
    evaluador = get_object_or_404(Trabajador, id_trabajador=evaluador_id)
    evaluado = get_object_or_404(Trabajador, id_trabajador=evaluado_id)
    
    autoeval_lista = Autoevaluacion.objects.filter(
        trabajador=evaluado, 
        estado_finalizacion=True
    ).exists()

    if not autoeval_lista:
        return redirect(f"/?id={evaluador_id}")

    if not dimension:
        respuestas = EvaluacionJefatura.objects.filter(evaluador=evaluador, trabajador_evaluado=evaluado)
        ya_finalizado = respuestas.filter(estado_finalizacion=True).exists()
        
        total_preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=evaluado.nivel_jerarquico).count()
        total_respuestas = respuestas.count()
        
        listo_para_enviar = (total_respuestas >= total_preguntas) and not ya_finalizado
        
        hecho_org = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional").exists()
        hecho_fun = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional").exists()
        
        return render(request, 'cuestionario/evaluacion_jefe_seleccion.html', {
            'evaluador': evaluador,
            'evaluado': evaluado,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun,
            'listo_para_enviar': listo_para_enviar,
            'ya_finalizado': ya_finalizado
        })

    ya_respondido = EvaluacionJefatura.objects.filter(
        evaluador=evaluador,
        trabajador_evaluado=evaluado,
        codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension
    ).exists()

    if ya_respondido:
        return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador.id_trabajador, evaluado_id=evaluado.id_trabajador)

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('id_textos_evaluacion')

    descripciones_qs = DescripcionRespuesta.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico
    ).select_related('escala')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
                    obj_escala = Escala.objects.get(id_escala=int(puntaje_valor))
                    
                    EvaluacionJefatura.objects.update_or_create(
                        evaluador=evaluador,
                        trabajador_evaluado=evaluado,
                        codigo_excel=pregunta,
                        defaults={
                            'puntaje': puntaje_valor,
                            'escala': obj_escala,
                            'fecha_evaluacion': timezone.now().date(),
                            'momento_evaluacion': timezone.now(),
                            'comentario': request.POST.get('comentario', ''),
                            'estado_finalizacion': False,
                            'nivel_jerarquico': pregunta.nivel_jerarquico
                        }
                    )
        return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador.id_trabajador, evaluado_id=evaluado.id_trabajador)

    context = {
        'evaluador': evaluador, 
        'evaluado': evaluado, 
        'preguntas': preguntas_qs, 
        'dimension': dimension,
        'descripciones': descripciones_qs
    }
    return render(request, 'cuestionario/evaluacion_jefe.html', context)

def finalizar_evaluacion_jefe(request, evaluador_id, evaluado_id):
    if request.method == "POST":
        EvaluacionJefatura.objects.filter(
            evaluador_id=evaluador_id, 
            trabajador_evaluado_id=evaluado_id
        ).update(estado_finalizacion=True)
        
        evaluado_obj = Trabajador.objects.get(id_trabajador=evaluado_id)
        generar_consolidado(evaluado_obj)
        
    return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador_id, evaluado_id=evaluado_id)