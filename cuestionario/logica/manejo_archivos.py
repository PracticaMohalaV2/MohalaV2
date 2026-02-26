from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from cuestionario.models import Biblioteca


@login_required
def ver_archivo_biblioteca(request, biblioteca_id):
    if not request.user.is_superuser:
        return redirect('index')
    try:
        doc = Biblioteca.objects.get(id_biblioteca=biblioteca_id)
    except Biblioteca.DoesNotExist:
        return redirect('index')
    response = HttpResponse(bytes(doc.archivo), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{doc.nombre}.pdf"'
    return response