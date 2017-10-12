from django import forms
from .models import *


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        exclude = {""}


class UPC(forms.Form):
    upc = forms.CharField(max_length=64)
