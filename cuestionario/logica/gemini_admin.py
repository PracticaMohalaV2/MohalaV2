from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cuestionario.models import PromptGemini
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


@login_required
def panel_gemini(request):
    """Panel principal de administración de Gemini"""
    if not request.user.is_superuser:
        return redirect('index')
    
    # Obtener el último prompt usado
    ultimo_prompt = PromptGemini.objects.first()
    
    # Obtener historial (últimos 20)
    historial = PromptGemini.objects.all()[:20]
    
    context = {
        'ultimo_prompt': ultimo_prompt,
        'historial': historial
    }
    
    return render(request, 'cuestionario/gemini_admin.html', context)


@login_required
def editar_prompt(request):
    """Editar y guardar nuevo prompt"""
    if not request.user.is_superuser:
        return redirect('index')
    
    if request.method == 'POST':
        prompt_texto = request.POST.get('prompt_texto', '')
        
        if prompt_texto.strip():
            # Crear nuevo prompt
            PromptGemini.objects.create(
                prompt_texto=prompt_texto
            )
            
            return redirect('panel_gemini')
    
    return redirect('panel_gemini')


@login_required
def generar_informe_gemini(request, prompt_id):
    """Generar informe usando Gemini y crear PDF"""
    if not request.user.is_superuser:
        return redirect('index')
    
    try:
        prompt_obj = PromptGemini.objects.get(id_prompt=prompt_id)
    except PromptGemini.DoesNotExist:
        return HttpResponse("Prompt no encontrado", status=404)
    
    try:
        # MODIFICADO: Usar models/gemini-2.0-flash (disponible en tu API key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Generar respuesta
        response = model.generate_content(prompt_obj.prompt_texto)
        respuesta_texto = response.text
        
        # Guardar respuesta en la BD
        prompt_obj.respuesta_gemini = respuesta_texto
        prompt_obj.pdf_generado = True
        prompt_obj.save()
        
        # Generar PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch, leftMargin=1*inch, rightMargin=1*inch)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#5e42a6'),
            spaceAfter=20,
            alignment=1  # Center
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=14
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#2196F3'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        # Título
        elements.append(Paragraph("Informe Generado por Gemini AI", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Fecha
        fecha_generacion = prompt_obj.timestamp.strftime("%d/%m/%Y %H:%M")
        elements.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_generacion}", body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Prompt usado
        elements.append(Paragraph("Prompt Utilizado", subtitle_style))
        elements.append(Paragraph(prompt_obj.prompt_texto, body_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Respuesta de Gemini
        elements.append(Paragraph("Informe Generado", title_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Procesar la respuesta (limpiar markdown básico)
        lineas = respuesta_texto.split('\n')
        for linea in lineas:
            if linea.strip():
                # Limpiar markdown
                linea_limpia = linea.replace('**', '<b>').replace('**', '</b>')
                linea_limpia = linea_limpia.replace('*', '<i>').replace('*', '</i>')
                linea_limpia = linea_limpia.replace('#', '')
                
                # Detectar si es un título (empieza con ##)
                if linea.strip().startswith('##'):
                    elements.append(Paragraph(linea_limpia.strip(), subtitle_style))
                else:
                    elements.append(Paragraph(linea_limpia, body_style))
        
        # Construir PDF
        doc.build(elements)
        
        # Crear respuesta
        pdf = buffer.getvalue()
        buffer.close()
        
        response_http = HttpResponse(pdf, content_type='application/pdf')
        response_http['Content-Disposition'] = f'inline; filename="informe_gemini_{prompt_id}.pdf"'
        
        return response_http
        
    except Exception as e:
        # Mostrar el error
        error_msg = f"ERROR al generar informe: {str(e)}"
        print(error_msg)
        
        # Guardar error en BD
        prompt_obj.respuesta_gemini = error_msg
        prompt_obj.save()
        
        # Devolver error como HTML
        return HttpResponse(f"""
            <html>
            <body style="font-family: Arial; padding: 40px;">
                <h1 style="color: #ff5151;">Error al generar PDF</h1>
                <p><strong>Detalles del error:</strong></p>
                <pre style="background: #f0f0f0; padding: 20px; border-radius: 5px;">{error_msg}</pre>
                <br>
                <a href="/gemini/" style="background: #5e42a6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Volver al Panel Gemini</a>
            </body>
            </html>
        """, status=500)


@login_required
def listar_modelos(request):
    """Listar modelos disponibles en tu API key"""
    if not request.user.is_superuser:
        return redirect('index')
    
    try:
        modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        
        return HttpResponse(f"""
            <html>
            <body style="font-family: Arial; padding: 40px;">
                <h1>Modelos disponibles con tu API key:</h1>
                <ul>
                    {''.join([f'<li>{m}</li>' for m in modelos])}
                </ul>
                <br>
                <a href="/gemini/">Volver</a>
            </body>
            </html>
        """)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")