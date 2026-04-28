from django import forms
from apps.recepten.models import Recept, ReceptIngredient, Ingredient
from django.forms import inlineformset_factory, ModelChoiceField
from apps.recepten.forms.fields import MinutenDurationField
from django_ckeditor_5.widgets import CKEditor5Widget
 
class ReceptForm(forms.ModelForm):

    bereidingswijze = forms.CharField(
        widget=CKEditor5Widget(config_name='default')
    )

    baktijd = MinutenDurationField(
            required=True,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '00:30'
                }
            ),
            help_text="Gebruik MM of HH:MM ( bijv. 30 of 01:15)"
    )


    class Meta:
        model = Recept
        fields = ['naam', 'categorie', 'bereidingswijze', 'baktijd', 'moeilijkheidsgraad', 'foto']
        widgets = {
            'naam': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
#            'bereidingswijze': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'moeilijkheidsgraad': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
 

