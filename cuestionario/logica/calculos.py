from django.db.models import Avg
from datetime import datetime
from cuestionario.models import Autoevaluacion, EvaluacionJefatura, ResultadoConsolidado, Trabajador

def generar_consolidado(trabajador, periodo=None):
    if not periodo:
        periodo = datetime.now().year

    # 1. Obtener todas las respuestas de autoevaluación finalizadas
    respuestas_auto = Autoevaluacion.objects.filter(trabajador=trabajador, estado_finalizacion=True)
    
    if not respuestas_auto.exists():
        return

    # 2. Verificar si el trabajador tiene un jefe asignado
    tiene_jefe = trabajador.id_jefe_directo is not None

    # 3. Obtener respuestas de la jefatura (si aplica)
    respuestas_jefe = EvaluacionJefatura.objects.filter(
        trabajador_evaluado=trabajador, 
        estado_finalizacion=True
    )

    # 4. Cálculo del Promedio General (COMENTADO DE MOMENTO)
    # if tiene_jefe and respuestas_jefe.exists():
    #     prom_gral = respuestas_jefe.aggregate(Avg('puntaje'))['puntaje__avg']
    # else:
    #     prom_gral = respuestas_auto.aggregate(Avg('puntaje'))['puntaje__avg']

    # 5. Iterar sobre cada pregunta de la autoevaluación para cruzar datos
    for r_auto in respuestas_auto:
        p_jefe = 0
        diff = 0
        
        # LÓGICA DE CRUCE:
        if tiene_jefe and respuestas_jefe.exists():
            # Si tiene jefe, buscamos la respuesta espejo
            r_jefe = respuestas_jefe.filter(codigo_excel=r_auto.codigo_excel).first()
            if r_jefe:
                p_jefe = r_jefe.puntaje
                diff = p_jefe - r_auto.puntaje
        else:
            # SI NO TIENE JEFE: Forzamos puntaje jefe y diferencia a 0
            p_jefe = 0
            diff = 0

        pregunta = r_auto.codigo_excel 
        comp = pregunta.competencia
        dim = comp.dimension

        # Calcular promedios específicos (COMENTADO DE MOMENTO)
        # if tiene_jefe and respuestas_jefe.exists():
        #     prom_dim = respuestas_jefe.filter(codigo_excel__competencia__dimension=dim).aggregate(Avg('puntaje'))['puntaje__avg']
        #     prom_comp = respuestas_jefe.filter(codigo_excel__competencia=comp).aggregate(Avg('puntaje'))['puntaje__avg']
        # else:
        #     prom_dim = respuestas_auto.filter(codigo_excel__competencia__dimension=dim).aggregate(Avg('puntaje'))['puntaje__avg']
        #     prom_comp = respuestas_auto.filter(codigo_excel__competencia=comp).aggregate(Avg('puntaje'))['puntaje__avg']

        # 6. Guardar o actualizar en la tabla ResultadoConsolidado
        ResultadoConsolidado.objects.update_or_create(
            trabajador=trabajador,
            codigo_excel=pregunta,
            periodo=periodo,
            defaults={
                'puntaje_autoev': r_auto.puntaje,
                'puntaje_jefe': p_jefe,
                'diferencia': diff,
                # 'prom_competencia': prom_comp,
                # 'prom_dimension': prom_dim,
                # 'prom_general': prom_gral,
                'dimension': dim,
                'competencia': comp,
                'nivel_jerarquico': r_auto.nivel_jerarquico,
            }
        )