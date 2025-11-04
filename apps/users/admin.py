from django.contrib import admin                                                                                                                                                    
from django.contrib.auth.models import User
from .models import UserProfile
 
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "excluded_from_reports")
    search_fields = ("user__username", "user__email")
    list_filter = ("excluded_from_reports",)
