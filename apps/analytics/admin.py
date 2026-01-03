from django.contrib import admin
from .models import DailyVisit
from .models import ReceptViewCount

@admin.register(DailyVisit)
class DailyVisitAdmin(admin.ModelAdmin):
    list_display = ("date", "count")
    ordering = ("-date",)

@admin.register(ReceptViewCount)
class ReceptViewCountAdmin1(admin.ModelAdmin):
    list_display = ("recept", "count")
    ordering = ("-count",)

