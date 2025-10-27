from django.contrib import admin                                                                                                                                                    
from .models import Recept, Ingredient, ReceptIngredient
 
class ReceptIngredientInline(admin.TabularInline):
    model = ReceptIngredient
    extra = 1  # aantal lege rijen dat standaard wordt getoond
    autocomplete_fields = ['ingredient']  # handig bij veel ingrediënten
 
@admin.register(Recept)
class ReceptAdmin(admin.ModelAdmin):
    list_display = ('naam', 'categorie', 'moeilijkheidsgraad', 'baktijd', 'datum_toegevoegd')
    list_filter = ('categorie', 'moeilijkheidsgraad')
    search_fields = ('naam', 'bereidingswijze')
    inlines = [ReceptIngredientInline]
 
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('naam',)

