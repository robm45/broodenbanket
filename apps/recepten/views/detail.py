from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from apps.recepten.models import Recept
from apps.analytics.models import ReceptViewCount


class ReceptDetailView(DetailView):
    model = Recept
    template_name = "recepten/recept_detail.html"
    context_object_name = "recept"

    def get_object(self, queryset=None):
        recept = super().get_object(queryset)

        # view count verhogen (AVG-proof)
        view_count, created = ReceptViewCount.objects.get_or_create(
            recept=recept
        )
        
        view_count.count += 1
        view_count.save(update_fields=["count"])

        return recept

