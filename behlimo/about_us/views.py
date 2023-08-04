from django.http import Http404
from django.views.generic import DetailView
from .models import AboutUs


class AboutUsPage(DetailView):
    model = AboutUs
    context_object_name = 'aboutus'

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(
                is_enabled=True
            )

        except self.model.DoesNotExist:
            raise Http404

        except self.model.MultipleObjectsReturned:
            raise Http404  # It's possible to implement other logic
