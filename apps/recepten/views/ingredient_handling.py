from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy                                                                                                                                                
from django.views.generic import CreateView,ListView
from django.forms import inlineformset_factory
from django.db.models.deletion import RestrictedError

from ..models import Recept, ReceptIngredient, Ingredient
from ..forms import ReceptForm, IngredientForm, ReceptIngredientForm

import os, io

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'recepten/ingredient_lijst.html'
    context_object_name = 'ingredienten'
    
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
    from apps.recepten.forms import VerwijderIngredientForm
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

