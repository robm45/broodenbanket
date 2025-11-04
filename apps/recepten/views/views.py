from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import redirect
from ..models import Recept, ReceptIngredient, Ingredient
from ..forms import ReceptForm, IngredientForm, ReceptIngredientForm
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
from ..models import Recept

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

