from django import forms
from .models import ImageUpload
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class PhotoUpload(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'image']

