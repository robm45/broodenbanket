import os                                                                                                                                                                           
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.shortcuts import redirect, render, get_object_or_404

def recept_image_path(instance, filename):
    # Haal bestandsextensie van de upload
    ext = filename.split('.')[-1]
    # Maak receptnaam "veilig" (spaties → underscores, lowercase)
    safe_name = instance.naam.replace(" ", "_").lower()
    # Bestandsnaam is gewoon de receptnaam met juiste extensie
    filename = f"{safe_name}.{ext}"
    # Opslag in submap per recept
    return os.path.join('recepten/images', safe_name, filename)
