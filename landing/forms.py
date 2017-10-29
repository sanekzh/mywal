from django import forms

from .models import *


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'


class UPC(forms.Form):
    upc = forms.CharField(max_length=64)


class Products(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'