from django.views.generic import ListView
from ..models import Recept, ReceptIngredient, Ingredient

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
