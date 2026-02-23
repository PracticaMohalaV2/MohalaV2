from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cuestionario.models import Trabajador, ResultadoConsolidado, ReporteGlobal
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from io import BytesIO
from datetime import datetime


@login_required
def generar_reporte_global_pdf(request):
    """Generar un PDF con todos los reportes individuales concatenados"""
    if not request.user.is_superuser:
        return redirect('index')
    
    # Obtener todos los trabajadores con evaluaciones completas
    trabajadores = Trabajador.objects.filter(
        resultados_consolidados__isnull=False
    ).select_related(
        'cargo', 
        'nivel_jerarquico', 
        'id_jefe_directo'
    ).distinct().order_by('apellido_paterno', 'nombre')
    
    if not trabajadores.exists():
        return HttpResponse("No hay trabajadores con evaluaciones completadas", status=404)
    
    # Crear PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=10,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2196F3'),
        spaceAfter=8,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=10,
        spaceBefore=15
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=5
    )
    
    # PORTADA DEL REPORTE GLOBAL
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("REPORTE GLOBAL DE EVALUACIONES DE DESEMPEÑO", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Total de Colaboradores: {trabajadores.count()}", subtitle_style))
    elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"Periodo: 2026", normal_style))
    elements.append(PageBreak())
    
    # Iterar sobre cada trabajador y generar su reporte individual
    for idx, trabajador in enumerate(trabajadores, 1):
        # Obtener resultados consolidados del trabajador
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
        from cuestionario.models import Autoevaluacion, EvaluacionJefatura
        
        auto = Autoevaluacion.objects.filter(
            trabajador=trabajador, 
            estado_finalizacion=True
        ).order_by('-momento_evaluacion').first()
        
        jefe = EvaluacionJefatura.objects.filter(
            trabajador=trabajador,
            estado_finalizacion=True
        ).order_by('-momento_evaluacion').first()
        
        # ENCABEZADO DEL TRABAJADOR
        elements.append(Paragraph(f"Reporte de Evaluación de Desempeño #{idx}", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Info del colaborador
        info_data = [
            [Paragraph("<b>Colaborador:</b>", normal_style), Paragraph(f"{trabajador.nombre} {trabajador.apellido_paterno} {trabajador.apellido_materno}", normal_style)],
            [Paragraph("<b>Cargo:</b>", normal_style), Paragraph(trabajador.cargo.nombre_cargo, normal_style)],
            [Paragraph("<b>Nivel:</b>", normal_style), Paragraph(trabajador.nivel_jerarquico.nombre_nivel_jerarquico, normal_style)],
            [Paragraph("<b>Jefatura Directa:</b>", normal_style), Paragraph(f"{trabajador.id_jefe_directo.nombre} {trabajador.id_jefe_directo.apellido_paterno}" if trabajador.id_jefe_directo else "N/A", normal_style)],
            [Paragraph("<b>Autoevaluación finalizada:</b>", normal_style), Paragraph(auto.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if auto else "N/A", normal_style)],
            [Paragraph("<b>Evaluación Jefatura finalizada:</b>", normal_style), Paragraph(jefe.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if jefe else "N/A", normal_style)],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Agrupar resultados por dimensión
        dimensiones = {}
        for resultado in resultados:
            dim_nombre = resultado.dimension.nombre_dimension
            if dim_nombre not in dimensiones:
                dimensiones[dim_nombre] = []
            dimensiones[dim_nombre].append(resultado)
        
        # Generar tabla para cada dimensión
        for dimension_nombre, resultados_dim in dimensiones.items():
            elements.append(Paragraph(f"Dimensión: {dimension_nombre}", heading_style))
            
            data = [
                [
                    Paragraph("<b>Código</b>", normal_style),
                    Paragraph("<b>Competencia</b>", normal_style),
                    Paragraph("<b>AutoEv</b>", normal_style),
                    Paragraph("<b>Ev. Jefe</b>", normal_style),
                    Paragraph("<b>Diferencia</b>", normal_style)
                ]
            ]
            
            for resultado in resultados_dim:
                data.append([
                    Paragraph(resultado.codigo_excel.codigo_excel, normal_style),
                    Paragraph(resultado.competencia.nombre_competencia, normal_style),
                    Paragraph(str(resultado.puntaje_autoev), normal_style),
                    Paragraph(str(resultado.puntaje_jefe) if resultado.puntaje_jefe else "N/A", normal_style),
                    Paragraph(str(resultado.diferencia), normal_style)
                ])
            
            table = Table(data, colWidths=[0.8*inch, 2.5*inch, 0.8*inch, 0.8*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5e42a6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Agregar salto de página entre trabajadores (excepto el último)
        if idx < trabajadores.count():
            elements.append(PageBreak())
    
    # Construir PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Guardar en BD
    reporte_global = ReporteGlobal.objects.create(
        contenido_pdf=pdf_bytes,
        total_trabajadores=trabajadores.count(),
        periodo=2026
    )
    
    # Devolver PDF al navegador
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_global_{reporte_global.id_reporte_global}.pdf"'
    
    return response