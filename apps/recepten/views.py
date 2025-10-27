from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import redirect
from .models import Recept, ReceptIngredient, Ingredient
from .forms import ReceptForm, IngredientForm, ReceptIngredientForm
from django.forms import inlineformset_factory
from django.db.models.deletion import RestrictedError
from django.contrib import messages
from weasyprint import HTML, CSS
from django.conf import settings
from django.template.loader import render_to_string
from PIL import Image
from django.core.files.base import ContentFile
import os, io


def home(request):
    return render(request, "recepten/home.html")

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Recept

# Lijstview generiek
class ReceptCategorieListView(ListView):
    model = Recept
    template_name = "recepten/recept_lijst.html"
    context_object_name = "recepten"
    paginate_by = 20
    ordering = ["naam"]

    def get_queryset(self):
        categorie = self.kwargs.get("categorie")
        return Recept.objects.filter(categorie=categorie)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorie = self.kwargs.get("categorie")
        context["titel"] = f"{categorie.capitalize()} Recepten"
        return context


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'recepten/ingredient_lijst.html'
    context_object_name = 'ingredienten'

# Detailview voor een recept (voor zowel brood als banket)
class ReceptDetailView(DetailView):
    model = Recept
    template_name = 'recepten/recept_detail.html'
    context_object_name = 'recept'


# invoer view voor nieuwe recpeten
class BaseReceptMixin:
    model = Recept
    form_class = ReceptForm
    template_name = "recepten/recept_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['ingredienten_formset'] = ReceptIngredientFormSet(
                self.request.POST,
                instance=self.object if hasattr(self, "object") else None 
            )
            data['new_ingredient_form'] = IngredientForm(self.request.POST)
        else:
            data['ingredienten_formset'] = ReceptIngredientFormSet(
                instance=self.object if hasattr(self, "object") else None
            )
            data['new_ingredient_form'] = IngredientForm()
        return data

    def form_valid(self, form):
                # FOTO VERWERKEN
        self.object = form.save(commit=False)  # recept opslaan
        self.object.save()

        print(self.request.FILES)
        foto = form.cleaned_data.get('foto')
        print("Foto in cleaned_data:", foto )
        if foto:
            # sla het orginele pad op
            orig_path = None
            if self.object.foto and self.object.foto.name:
                orig_path = self.object.foto.path

           # verwerk met Pillow
            img = Image.open(foto)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.thumbnail((800, 800))

            buffer = io.BytesIO()
            img.save(fp=buffer, format='JPEG')
            buffer.seek(0)

            filename = os.path.basename(foto.name)
        
            self.object.foto.save(filename, ContentFile(buffer.read()), save=True)
            # Verwijder origineel als het een andere file is
            if orig_path and os.path.exists(orig_path) and orig_path != self.object.foto.path:
                os.remove(orig_path)

        
        # Formset verwerken
        ingredienten_formset = ReceptIngredientFormSet(self.request.POST, instance=self.object)
        if ingredienten_formset.is_valid():
            for ingr_form in ingredienten_formset:
                if ingr_form.cleaned_data and not ingr_form.cleaned_data.get('DELETE', False):
                    nieuw_naam = ingr_form.cleaned_data.get("nieuw_ingredient")
                    if nieuw_naam:
                        ingredient, _ = Ingredient.objects.get_or_create(naam=nieuw_naam)
                        ingr_form.instance.ingredient = ingredient
        ingredienten_formset.save()

        return redirect("recepten:recept-detail", pk=self.object.pk)




        print("MEDIA_ROOT =", settings.MEDIA_ROOT)
        if getattr(self, "object", None) and getattr(self.object, "foto", None):
             print("foto.name  =", self.object.foto.name)  # bijv. 'recepten_fotos/bestand.jpg'
             try:
                print("foto.path  =", self.object.foto.path)  # volledig pad op schijf
                print("foto.exists:", os.path.exists(self.object.foto.path))
             except NotImplementedError:
                print("Storage heeft geen lokaal pad (bv. cloud storage).")

        return redirect("recepten:recept-detail", pk=self.object.pk)


class ReceptCreateView(BaseReceptMixin, CreateView):
    """Nieuw recept maken"""
    model=Recept
 
class ReceptUpdateView(BaseReceptMixin, UpdateView):
    """Recept Update"""
    model=Recept

class ReceptDeleteView(DeleteView):
    model = Recept
    template_name = "recepten/recept_bevestig_verwijderen.html"
    success_url = reverse_lazy("home")

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recepten/ingredient_toevoegen.html'
    success_url = reverse_lazy('recepten:ingredient-lijst')


# formset voor de gecombineerde invoer van recept inclusief de ingredienten
ReceptIngredientFormSet = inlineformset_factory (
        Recept,
        ReceptIngredient,
        fields=('ingredient','hoeveelheid'),
        extra=1,
        can_delete=True
)

def ingredient_verwijderen(request):
    from recepten.forms import VerwijderIngredientForm
    if request.method == 'POST':
        form = VerwijderIngredientForm(request.POST)
        if form.is_valid():
            geselecteerde_ingredienten = form.cleaned_data['ingredienten']
            for ct in geselecteerde_ingredienten:
                try:
                    ct.delete()
                    messages.success(request, f"Ingredient '{ct}' is verwijderd.")
                except RestrictedError:
                    messages.error(
                        request,
                        f"Ingredient '{ct}' kan niet worden verwijderd omdat het nog gekoppeld is aan één of meer recepten."
                    )
            return redirect('recepten:ingredient-lijst')  # of een andere url
    else:
        form = VerwijderIngredientForm()
    return render(request, 'recepten/ingredient_verwijderen.html', {'form': form})


def export_recept_pdf(request, pk):
    from recepten.models import Recept  # pas aan naar jouw app/model

    recept = Recept.objects.get(id=pk)

    if recept.foto:
       foto_pad = 'file://' + os.path.join(settings.BASE_DIR, recept.foto.name)
    else:
        foto_pad = None

    html_string = render_to_string(
       'recepten/recept_pdf.html',
       {'recept': recept, 'foto_pad': foto_pad}
    )
    
    if recept.foto:
        foto_url = request.build_absolute_uri(recept.foto.url)
    else:
        foto_url = None

    html_string = render_to_string(
       'recepten/recept_pdf.html',
       {'recept': recept, 'foto_url': foto_url}
    )



    # Render naar HTML string (gebruik de pdf template)
    html_string = render_to_string('recepten/recept_pdf.html', {'recept': recept})

    # CSS bestand laden
    css_file = os.path.join(settings.BASE_DIR, 'static', 'css', 'pdf.css')
    css = CSS(filename=css_file)

    # PDF genereren
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])

    # HTTP response teruggeven
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recept.naam}.pdf"'
    return response

