from django import forms
from django.forms import ModelMultipleChoiceField
from . import models


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = models.Exercise
        fields = ['name', 'video_embed', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'video_embed': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class WorkoutForm(forms.ModelForm):
    exercises = ModelMultipleChoiceField(
        queryset=models.Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = models.Workout
        fields = ['name', 'exercises']

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        choices = []
        for category in models.ExerciseCategory.objects.all():
            exercise_choices = [(exercise.id, exercise.name) for exercise in category.exercises.all()]
            if exercise_choices:
                choices.append((category.name, exercise_choices))
        self.fields['exercises'].choices = choices
