from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from apps.recepten.models import Recept, ReceptIngredient, Ingredient
from apps.recepten.forms import ReceptForm, IngredientForm, ReceptIngredientForm, ReceptIngredientFormSet, MinutenDurationField
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
                                
        #print(self.request.FILES)
        foto = form.cleaned_data.get('foto')
       # print("Foto in cleaned_data:", foto )
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
        ingredienten_formset = ReceptIngredientFormSet(
                self.request.POST, 
                instance=self.object
        )
        if ingredienten_formset.is_valid():
            instances = ingredienten_formset.save(commit=False)

            volgorde=0
            for ingr_form, instance in zip(ingredienten_formset.forms, instances):
                if ingr_form.cleaned_data.get('DELETE', False):
                    continue

                nieuw_naam = ingr_form.cleaned_data.get("nieuw_ingredient")
                if nieuw_naam:
                        ingredient, _ = Ingredient.objects.get_or_create(naam=nieuw_naam)
                        ingr_form.instance.ingredient = ingredient
                
                instance.rcept = self.object
                instance.save()

            for obj in ingredienten_formset.deleted_objects:
                obj.delete()

            qs = ReceptIngredient.objects.filter(
                    recept=self.object
            ).order_by("volgorde","id")

            for index, ri in enumerate(qs):
                if ri.volgorde != index:
                    ri.volgorde = index
                    ri.save(update_fields=["volgorde"])


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

    # views.py

    
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

# Volgorde wijziging

def ingredient_omhoog(request, ri_id):
    with transaction.atomic():
        ri = (
            ReceptIngredient.objects
            .select_for_update()
            .get(pk=ri_id)
        )

        boven = (
            ReceptIngredient.objects
            .select_for_update()
            .filter(
                recept=ri.recept,
                volgorde__lt=ri.volgorde
            )
            .order_by("-volgorde")
            .first()
        )

        if boven:
            ri.volgorde, boven.volgorde = boven.volgorde, ri.volgorde
            ri.save(update_fields=["volgorde"])
            boven.save(update_fields=["volgorde"])

    return redirect("recepten:recept-update", pk=ri.recept.pk)

                            
def ingredient_omlaag(request, ri_id):
    with transaction.atomic():
        ri = (
            ReceptIngredient.objects
            .select_for_update()
            .get(pk=ri_id)
        )

        onder = (
            ReceptIngredient.objects
            .select_for_update()
            .filter(
                recept=ri.recept,
                volgorde__gt=ri.volgorde
            )
            .order_by("volgorde")
            .first()
        )

        if onder:
            ri.volgorde, onder.volgorde = onder.volgorde, ri.volgorde
            ri.save(update_fields=["volgorde"])
            onder.save(update_fields=["volgorde"])

    return redirect("recepten:recept-update", pk=ri.recept.pk)

                                
