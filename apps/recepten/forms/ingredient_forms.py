from django import forms                                                                                                                                                              
from apps.recepten.models import Recept, ReceptIngredient, Ingredient
from django.forms import inlineformset_factory, ModelChoiceField
 
 
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['naam']
        widgets = {
            'naam': forms.TextInput(attrs={'class': 'form-control'}),
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_field = next(iter(self.fields.values()))
        first_field.widget.attrs["autofocus"] = True
 
class ReceptIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
            queryset=Ingredient.objects.all(),
            empty_label="Kies een ingredient",
            required=False
    )
 
    nieuw_ingredient = forms.CharField(
            required=False,
            label="Nieuw ingredient",
            help_text="Voer een nieuw ingredient in"
    )
 
    class Meta:
        model = ReceptIngredient
        fields = ['ingredient','hoeveelheid','eenheid', 'nieuw_ingredient']
 
class VerwijderIngredientForm(forms.Form):
    ingredienten=forms.ModelMultipleChoiceField(
            queryset=Ingredient.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
     )
 
 
IngredientFormSet = inlineformset_factory(
    Recept,
    ReceptIngredient,
    fields=['ingredient', 'hoeveelheid', 'eenheid'],
    extra=1,  # standaard 3 lege velden
    can_delete=True,
    widgets={
        'naam': forms.TextInput(attrs={'class': 'form-control'}),
        'hoeveelheid': forms.TextInput(attrs={'class': 'form-control'}),
        'eenheid': forms.TextInput(attrs={'class': 'form-control'}),
    }
)
 
ReceptIngredientFormSet = inlineformset_factory(
    Recept,
    ReceptIngredient,
    form=ReceptIngredientForm,
    extra=1,
    can_delete=True
)
 

