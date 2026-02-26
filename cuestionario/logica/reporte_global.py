from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cuestionario.models import (Trabajador, Autoevaluacion, EvaluacionJefatura, ResultadoConsolidado, ReporteGlobal)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape


@login_required
def generar_reporte_global_pdf(request):
    """Genera un PDF global con todos los reportes individuales concatenados usando ReportLab"""

    if not request.user.is_superuser:
        return redirect('index')

    trabajadores = Trabajador.objects.filter(
        resultadoconsolidado__isnull=False
    ).select_related(
        'cargo',
        'nivel_jerarquico',
        'id_jefe_directo'
    ).distinct().order_by('apellido_paterno', 'nombre')

    if not trabajadores.exists():
        return HttpResponse("No hay trabajadores con evaluaciones completadas.", status=404)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'GlobalTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    portada_style = ParagraphStyle(
        'GlobalPortada',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'GlobalHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#51ff85'),
        spaceAfter=12,
        spaceBefore=20
    )
    func_heading_style = ParagraphStyle(
        'GlobalFuncHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2196F3'),
        spaceAfter=12,
        spaceBefore=20
    )
    comp_style = ParagraphStyle(
        'GlobalCompStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#5e42a6'),
        fontName='Helvetica-Bold',
        spaceAfter=2,
    )
    comp_func_style = ParagraphStyle(
        'GlobalCompFuncStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#2196F3'),
        fontName='Helvetica-Bold',
        spaceAfter=2,
    )
    indicator_style = ParagraphStyle(
        'GlobalIndicatorStyle',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.HexColor('#555555'),
        leading=9,
    )

    # Crear el reporte en BD primero para obtener el ID
    reporte_global_temp = ReporteGlobal.objects.create(
        contenido_pdf=b'',  # Temporal vacío
        total_trabajadores=trabajadores.count(),
        periodo=2026
    )

    # PORTADA
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph("REPORTE GLOBAL DE EVALUACIONES DE DESEMPEÑO", portada_style))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"ID Reporte: #{reporte_global_temp.id_reporte_global}", title_style))
    elements.append(Paragraph(f"Total de Colaboradores: {trabajadores.count()}", title_style))
    elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", title_style))
    elements.append(Paragraph("Periodo: 2026", title_style))
    elements.append(PageBreak())

    total = trabajadores.count()

    for idx, trabajador in enumerate(trabajadores, 1):

        resultados = ResultadoConsolidado.objects.filter(
            trabajador=trabajador
        ).select_related(
            'codigo_excel', 'competencia', 'dimension'
        ).order_by('codigo_excel__id_textos_evaluacion')

        if not resultados.exists():
            continue

        resultados_organizacionales = resultados.filter(
            dimension__nombre_dimension__icontains='Organizacional'
        )
        resultados_funcionales = resultados.filter(
            dimension__nombre_dimension__icontains='Funcional'
        )

        auto = Autoevaluacion.objects.filter(
            trabajador=trabajador, estado_finalizacion=True
        ).first()
        jefe = EvaluacionJefatura.objects.filter(
            trabajador_evaluado=trabajador, estado_finalizacion=True
        ).first()

        timestamp_auto = auto.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if auto else "Pendiente"
        timestamp_jefe = jefe.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if jefe else "N/A"

        elements.append(
            Paragraph(f"Reporte de Evaluación de Desempeño — #{idx} de {total}", title_style)
        )
        elements.append(Spacer(1, 0.2 * inch))

        jefe_directo_nombre = (
            f"{trabajador.id_jefe_directo.nombre} "
            f"{trabajador.id_jefe_directo.apellido_paterno} "
            f"{trabajador.id_jefe_directo.apellido_materno}"
            if trabajador.id_jefe_directo else "N/A"
        )

        info_data = [
            ['Colaborador:',                    f"{trabajador.nombre} {trabajador.apellido_paterno} {trabajador.apellido_materno}"],
            ['Cargo:',                          trabajador.cargo.nombre_cargo],
            ['Nivel:',                          trabajador.nivel_jerarquico.nombre_nivel_jerarquico],
            ['Jefatura Directa:',               jefe_directo_nombre],
            ['Autoevaluación finalizada:',      timestamp_auto],
            ['Evaluación Jefatura finalizada:', timestamp_jefe],
        ]

        info_table = Table(info_data, colWidths=[2.5 * inch, 4 * inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR',     (0, 0), (-1, -1), colors.black),
            ('ALIGN',         (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME',      (0, 0), (0, -1),  'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING',    (0, 0), (-1, -1), 8),
            ('GRID',          (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Tabla Organizacional
        elements.append(Paragraph("Dimensión: Organizacional", heading_style))

        org_data = [['Código', 'Competencia / Indicador', 'AutoEv', 'Ev. Jefe', 'Diferencia']]
        for r in resultados_organizacionales:
            celda = [
                Paragraph(escape(r.competencia.nombre_competencia), comp_style),
                Paragraph(escape(r.codigo_excel.texto), indicator_style),
            ]
            org_data.append([
                r.codigo_excel.codigo_excel,
                celda,
                str(r.puntaje_autoev),
                str(r.puntaje_jefe) if r.puntaje_jefe > 0 else 'N/A',
                f"{'+' if r.diferencia > 0 else ''}{int(r.diferencia)}",
            ])

        org_table = Table(org_data, colWidths=[0.7 * inch, 3.2 * inch, 0.7 * inch, 0.7 * inch, 0.8 * inch])
        org_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#5e42a6')),
            ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN',         (1, 0), (1, -1),  'LEFT'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('VALIGN',        (1, 1), (1, -1),  'TOP'),
            ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, 0),  10),
            ('FONTSIZE',      (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING',    (0, 0), (-1, -1), 6),
            ('GRID',          (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(org_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Tabla Funcional
        elements.append(Paragraph("Dimensión: Funcional", func_heading_style))

        func_data = [['Código', 'Competencia / Indicador', 'AutoEv', 'Ev. Jefe', 'Diferencia']]
        for r in resultados_funcionales:
            celda = [
                Paragraph(escape(r.competencia.nombre_competencia), comp_func_style),
                Paragraph(escape(r.codigo_excel.texto), indicator_style),
            ]
            func_data.append([
                r.codigo_excel.codigo_excel,
                celda,
                str(r.puntaje_autoev),
                str(r.puntaje_jefe) if r.puntaje_jefe > 0 else 'N/A',
                f"{'+' if r.diferencia > 0 else ''}{int(r.diferencia)}",
            ])

        func_table = Table(func_data, colWidths=[0.7 * inch, 3.2 * inch, 0.7 * inch, 0.7 * inch, 0.8 * inch])
        func_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#5e42a6')),
            ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN',         (1, 0), (1, -1),  'LEFT'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('VALIGN',        (1, 1), (1, -1),  'TOP'),
            ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, 0),  10),
            ('FONTSIZE',      (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING',    (0, 0), (-1, -1), 6),
            ('GRID',          (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(func_table)

        if idx < total:
            elements.append(PageBreak())

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Actualizar el reporte con el PDF generado
    reporte_global_temp.contenido_pdf = pdf_bytes
    reporte_global_temp.save()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'inline; filename="reporte_respuestas_global_{reporte_global_temp.id_reporte_global}.pdf"'
    )
    return response


@login_required
def ver_reporte_global_pdf(request, reporte_id):
    """Ver el PDF del reporte global guardado en la BD"""
    if not request.user.is_superuser:
        return redirect('index')
    
    try:
        reporte = ReporteGlobal.objects.get(id_reporte_global=reporte_id)
    except ReporteGlobal.DoesNotExist:
        return HttpResponse("Reporte no encontrado", status=404)
    
    if not reporte.contenido_pdf:
        return HttpResponse("Este reporte no tiene PDF generado", status=404)
    
    response = HttpResponse(reporte.contenido_pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_respuestas_global_{reporte_id}.pdf"'
    return response