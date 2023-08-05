from django import forms
from .models import Order
from ..tables.models import Table


class OrderForm(forms.Form):
    table = forms.ModelChoiceField(queryset=Table.objects.exclude(is_reserved=True), empty_label=None)
    customer_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={

    }))
