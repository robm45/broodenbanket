from django.db import models                                                                                                                                                        
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
 
    excluded_from_reports = models.BooleanField(
            default=False,
            verbose_name="Volledig uitgesloten van rapoortages",
            help_text="Deze gebruiker ontvangt nooit rapportage e-mails"
    )
 
    receive_monthly_mail = models.BooleanField(
            default=False,
            verbose_name="Ontvang maandelijks receptenmail",
            help_text="Als uitgeschakeld, ontvangt de gebruiker geen maandelijkse email met nieuwe recepten meer"
    )
 
 
    def __str__(self):
        return self.user.username
 
 
# ---- Automatisch aanmaken bij nieuwe gebruiker ----
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

