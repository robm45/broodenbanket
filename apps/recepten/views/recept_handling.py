from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from ..models import Recept, ReceptIngredient, Ingredient
from ..forms import ReceptForm, IngredientForm, ReceptIngredientForm, ReceptIngredientFormSet
from PIL import Image
from django.core.files.base import ContentFile
import os, io

# invoer view voor nieuwe recepten
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
    success_url = reverse_lazy("welkom")

# Detailview voor een recept (voor zowel brood als banket)                                                                                                                          
class ReceptDetailView(DetailView):
    model = Recept
    template_name = 'recepten/recept_detail.html'
    context_object_name = 'recept'

