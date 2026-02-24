from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura, ResultadoConsolidado, ReporteGlobal
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime


@login_required
def generar_reporte_global_pdf(request):
    """Genera un PDF con todos los reportes individuales concatenados usando ReportLab"""
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
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    portada_style = ParagraphStyle(
        'Portada',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#5e42a6'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#51ff85'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # PORTADA
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("REPORTE GLOBAL DE EVALUACIONES DE DESEMPEÑO", portada_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Total de Colaboradores: {trabajadores.count()}", title_style))
    elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", title_style))
    elements.append(Paragraph("Periodo: 2026", title_style))
    elements.append(PageBreak())
    
    # Iterar sobre cada trabajador
    for idx, trabajador in enumerate(trabajadores, 1):
        # Obtener resultados
        resultados = ResultadoConsolidado.objects.filter(
            trabajador=trabajador
        ).select_related('codigo_excel', 'competencia', 'dimension').order_by('codigo_excel__id_textos_evaluacion')
        
        if not resultados.exists():
            continue
        
        resultados_organizacionales = resultados.filter(dimension__nombre_dimension__icontains='Organizacional')
        resultados_funcionales = resultados.filter(dimension__nombre_dimension__icontains='Funcional')
        
        # Obtener fechas
        auto = Autoevaluacion.objects.filter(trabajador=trabajador, estado_finalizacion=True).first()
        jefe = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador, estado_finalizacion=True).first()
        
        timestamp_auto = auto.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if auto else "Pendiente"
        timestamp_jefe = jefe.momento_evaluacion.strftime("%d/%m/%Y %H:%M") if jefe else "N/A"
        
        # Título del trabajador
        elements.append(Paragraph(f"Reporte de Evaluación de Desempeño - #{idx}", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Información del trabajador
        jefe_directo_nombre = f"{trabajador.id_jefe_directo.nombre} {trabajador.id_jefe_directo.apellido_paterno} {trabajador.id_jefe_directo.apellido_materno}" if trabajador.id_jefe_directo else "N/A"
        
        info_data = [
            ['Colaborador:', f"{trabajador.nombre} {trabajador.apellido_paterno} {trabajador.apellido_materno}"],
            ['Cargo:', trabajador.cargo.nombre_cargo],
            ['Nivel:', trabajador.nivel_jerarquico.nombre_nivel_jerarquico],
            ['Jefatura Directa:', jefe_directo_nombre],
            ['Autoevaluación finalizada:', timestamp_auto],
            ['Evaluación Jefatura finalizada:', timestamp_jefe]
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla Organizacional
        elements.append(Paragraph("Dimensión: Organizacional", heading_style))
        
        org_data = [['Código', 'Competencia', 'AutoEv', 'Ev. Jefe', 'Diferencia']]
        for r in resultados_organizacionales:
            org_data.append([
                r.codigo_excel.codigo_excel,
                r.competencia.nombre_competencia,
                str(r.puntaje_autoev),
                str(r.puntaje_jefe) if r.puntaje_jefe > 0 else 'N/A',
                f"{'+' if r.diferencia > 0 else ''}{int(r.diferencia)}"
            ])
        
        org_table = Table(org_data, colWidths=[0.8*inch, 2.5*inch, 0.8*inch, 0.8*inch, 1*inch])
        org_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5e42a6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(org_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabla Funcional
        func_heading_style = ParagraphStyle(
            'FuncHeading',
            parent=heading_style,
            textColor=colors.HexColor('#2196F3')
        )
        elements.append(Paragraph("Dimensión: Funcional", func_heading_style))
        
        func_data = [['Código', 'Competencia', 'AutoEv', 'Ev. Jefe', 'Diferencia']]
        for r in resultados_funcionales:
            func_data.append([
                r.codigo_excel.codigo_excel,
                r.competencia.nombre_competencia,
                str(r.puntaje_autoev),
                str(r.puntaje_jefe) if r.puntaje_jefe > 0 else 'N/A',
                f"{'+' if r.diferencia > 0 else ''}{int(r.diferencia)}"
            ])
        
        func_table = Table(func_data, colWidths=[0.8*inch, 2.5*inch, 0.8*inch, 0.8*inch, 1*inch])
        func_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5e42a6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(func_table)
        
        # Salto de página entre trabajadores (excepto el último)
        if idx < trabajadores.count():
            elements.append(PageBreak())
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener bytes del PDF
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Guardar en BD
    reporte_global = ReporteGlobal.objects.create(
        contenido_pdf=pdf_bytes,
        total_trabajadores=trabajadores.count(),
        periodo=2026
    )
    
    # Crear respuesta
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_global_{reporte_global.id_reporte_global}.pdf"'
    
    return response