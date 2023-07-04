from django import forms
from . import models


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = models.Exercise
        fields = ['name', 'video_url', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
