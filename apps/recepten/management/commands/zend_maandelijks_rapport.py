from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from datetime import datetime
from django.conf import settings

from django.contrib.auth.models import User
from apps.recepten.models import Recept
from apps.users.models import UserProfile

import os

class Command(BaseCommand):
    help = "Verstuur een maandelijkse samenvatting van nieuwe recepten."

    def handle(self, *args, **options):
        # ----------------------------
        # Bereken vorige maand
        # ----------------------------
        today = datetime.now()
        first_of_this_month = today.replace(day=1)
#        last_month_end = first_of_this_month - timedelta(days=1)
#        last_month_start = last_month_end.replace(day=1)

        # Begin van de maand ( alleen in dev )
        # Eind = nu   ( alleen in dev )
        last_month_end =  today
        last_month_start = today.replace(day=1)


        self.stdout.write(
            f"Verzamel recepten van {last_month_start} t/m {last_month_end}"
        )

        # ----------------------------
        # Haal recepten op
        # ----------------------------
        new_recipes = Recept.objects.filter(
             datum_toegevoegd__gte=last_month_start,
             datum_toegevoegd__lte=last_month_end
        ).order_by("datum_toegevoegd")

        if not new_recipes.exists():
            self.stdout.write("Geen nieuwe recepten in de afgelopen maand.")
            return

        # ----------------------------
        # Bouw context
        # ----------------------------
        recepts = [
            {
                "naam": r.naam,
                "url": f"{settings.SITE_DOMAIN}/detail/{r.id}/",  # of reverse('recepten:detail', args=[r.id])
            }
            for r in new_recipes
        ]

        context = {
            "month": last_month_start.strftime("%B %Y"),
            "recepts": recepts,
            "site_domain": settings.SITE_DOMAIN,
        }

        # ----------------------------
        # Mailtemplates
        # ----------------------------
        text_content = render_to_string("recepten/emails/maandelijks_rapport.txt", context)
        html_content = render_to_string("recepten/emails/maandelijks_rapport.html", context)

        subject = f"Nieuwe recepten - {context['month']}"

        # ----------------------------
        # Selecteer ontvangers
        # ----------------------------
        recipients = User.objects.filter(
            is_active=True,
            profile__excluded_from_reports=False,
            profile__receive_monthly_mail=True,
        )

        if not recipients.exists():
            self.stdout.write("Geen ontvangers gevonden voor deze mailing.")
            return

        self.stdout.write(f"Verstuur rapport naar {recipients.count()} gebruikers...")

        # ----------------------------
        # Verstuur mails
        # ----------------------------
        for user in recipients:
            email = user.email
            if not email:
                continue

            msg = EmailMultiAlternatives(subject, text_content, to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        self.stdout.write("Maandelijkse mailing succesvol verstuurd.")

