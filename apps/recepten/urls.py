from django.urls import path, include
from . import views
from .views import ReceptDetailView, ReceptCreateView, IngredientListView, IngredientCreateView, ReceptUpdateView, ReceptDeleteView, ReceptCategorieListView
from .views import export_recept_pdf
from django.conf import settings
from django.conf.urls.static import static

app_name = 'recepten' 

urlpatterns = [
        path('recept/<int:pk>/', ReceptDetailView.as_view(), name='recept-detail'),
        path('recept/<int:pk>/update',ReceptUpdateView.as_view(), name='recept-update'),
        path('recept/<int:pk>/delete',ReceptDeleteView.as_view(), name='recept-delete'),
        path('nieuw/', ReceptCreateView.as_view(), name='recept-create'),
        path('ingredientlijst/', IngredientListView.as_view(), name='ingredient-lijst'),
        path('ingredientnieuw/', IngredientCreateView.as_view(), name='ingredient-toevoegen'), 
        path('ingredientverwijderen/', views.ingredient_verwijderen, name='ingredient-verwijderen'),
        path('recept/<int:pk>/export_pdf', views.export_recept_pdf, name='recept-export-pdf'),
        path('<str:categorie>/',ReceptCategorieListView.as_view(), name='recept-categorie-lijst'),
        path('recept/<int:pk>/',ReceptDetailView.as_view(), name='recept-detail'),
]

