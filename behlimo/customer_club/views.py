from django.views.generic import FormView
from .forms import CustomerForm


class RegisterCustomerView(FormView):
    form_class = CustomerForm
    template_name = 'home.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        super().form_valid(form)
