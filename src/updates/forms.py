from django import forms
from .models import Update as UpdateModel

class UpdateModelForm(forms.ModelForm): 
    class Meta:
        model = UpdateModel
        fields = [
            'user',
            'content',
            'image'
        ]