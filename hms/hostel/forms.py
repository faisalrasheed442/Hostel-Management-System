from django import forms
from .models import  customer

class ImageForm(forms.ModelForm):
    class Meta:
        model=customer
        fields='__all__'

