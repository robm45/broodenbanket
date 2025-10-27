from django import forms
from .models import Recept, ReceptIngredient, Ingredient
from django.forms import inlineformset_factory, ModelChoiceField


class ReceptForm(forms.ModelForm):
    class Meta:
        model = Recept
        fields = ['naam', 'categorie', 'bereidingswijze', 'baktijd', 'moeilijkheidsgraad', 'foto']
        widgets = {
            'naam': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'bereidingswijze': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'baktijd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00:30:00'}),
            'moeilijkheidsgraad': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['naam']
        widgets = {
            'naam': forms.TextInput(attrs={'class': 'form-control'}),
        }

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
        fields = ['ingredient','hoeveelheid','nieuw_ingredient']

class VerwijderIngredientForm(forms.Form):
    ingredienten=forms.ModelMultipleChoiceField(
            queryset=Ingredient.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
     )


IngredientFormSet = inlineformset_factory(
    Recept,
    ReceptIngredient,
    fields=['ingredient', 'hoeveelheid'],
    extra=1,  # standaard 3 lege velden
    can_delete=True,
    widgets={
        'naam': forms.TextInput(attrs={'class': 'form-control'}),
        'hoeveelheid': forms.TextInput(attrs={'class': 'form-control'}),
    }
)

ReceptIngredientFormSet = inlineformset_factory(
    Recept,
    ReceptIngredient,
    form=ReceptIngredientForm,
    extra=1,
    can_delete=True
)

