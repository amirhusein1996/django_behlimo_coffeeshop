from django.http import Http404
from django.views.generic import DetailView
from .models import ContactUs


class ContactUsPage(DetailView):
    model = ContactUs
    context_object_name = 'contactus'

    def get_object(self, queryset=None):
        contact_us = ContactUs.objects.first()
        if not contact_us:
            raise Http404
        return contact_us
