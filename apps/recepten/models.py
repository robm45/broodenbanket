from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from apps.recepten.utils import recept_image_path
 
class Ingredient(models.Model):
    naam = models.CharField(
            max_length=100,
            unique=True,
            help_text = "Vul hier een ingredient in",
    )
 
    def __str__(self):
        return self.naam
 
    def clean(self):
        super().clean()
        if Ingredient.objects.filter(naam__iexact=self.naam).exclude(pk=self.pk).exists():
            raise ValidationError({'naam': "Ingredient bestaat al (case insensitive match)"})
 
    def save(self, *args, **kwargs):
        self.full_clean()  # roept clean() aan, zorgt dat validatie gebeurt voor opslaan
        super().save(*args, **kwargs)
 
 
class Recept(models.Model):
    BROOD = 'brood'
    BANKET = 'banket'
 
    CATEGORIE_CHOICES = [
        (BROOD, 'Brood'),
        (BANKET, 'Banket'),
    ]
 
    MOEILIJKHEID_CHOICES = [
        (1, 'Makkelijk'),
        (2, 'Gemiddeld'),
        (3, 'Moeilijk'),
    ]
 
    naam = models.CharField(max_length=100)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES)
    bereidingswijze = models.TextField()
    baktijd = models.DurationField(help_text="Bijv. 00:30:00 voor 30 minuten")
    moeilijkheidsgraad = models.PositiveSmallIntegerField(choices=MOEILIJKHEID_CHOICES, default=1)
    datum_toegevoegd = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to=recept_image_path, blank=True, null=True)
 
    ingredienten = models.ManyToManyField(
        Ingredient,
        through='ReceptIngredient',
        related_name='recepten'
    )
 
    def __str__(self):
        return f"{self.naam} ({self.get_categorie_display()})"
 
    class Meta:
        ordering = ["naam"]
 
class ReceptIngredient(models.Model):
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    hoeveelheid = models.CharField(max_length=50, help_text="Bijv. '500g', '1 tl'")
 
    def __str__(self):
        return f"{self.hoeveelheid} {self.ingredient.naam} voor {self.recept.naam}"
 
