from django.utils.timezone import now
from .models import DailyVisit, ReceptViewCount

class DailySessionVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Zorg dat er een sessie is
        if not request.session.session_key:
            request.session.create()

        today = now().date()
        session_key = f"visited_{today}"

        # Alleen 1x per sessie per dag tellen
        if not request.session.get(session_key):
            visit, _ = DailyVisit.objects.get_or_create(date=today)
            visit.count += 1
            visit.save(update_fields=["count"])
            request.session[session_key] = True

        return self.get_response(request)


