from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os

def export_recept_pdf(request, pk):
    from ..models import Recept  # pas aan naar jouw app/model
 
    recept = Recept.objects.get(id=pk)
 
    if recept.foto:
       foto_pad = 'file://' + os.path.join(settings.MEDIA_ROOT, recept.foto.name)
    else:
        foto_pad = None
 
    print("📸 Foto pad:", foto_pad)  # <-- komt in je Django console terecht

    # Render naar HTML string (gebruik de pdf template)
    html_string = render_to_string(
       'recepten/recept_pdf.html',
       {'recept': recept, 'foto_pad': foto_pad}
    )
 
 
 
    # CSS bestand laden
    css_file = os.path.join(settings.BASE_DIR, 'static', 'css', 'pdf.css')
    css = CSS(filename=css_file)
 
    # PDF genereren
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
 
    # HTTP response teruggeven
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recept.naam}.pdf"'
    return response
