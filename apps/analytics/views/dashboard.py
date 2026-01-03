from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum

from apps.analytics.models import ReceptViewCount, DailyVisit
from apps.recepten.models import Recept


class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def test_func(self):
        return self.request.user.groups.filter(name="beheer").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # totaal bezoekers
        context["total_visits"] = (
            DailyVisit.objects.aggregate(total=Sum("count"))["total"] or 0
        )

        # meest bezochte recepten
        context["top_recepten"] = (
            ReceptViewCount.objects
            .select_related("recept")
            .order_by("-count")[:10]
        )

        return context

