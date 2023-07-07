from django import forms
from django.forms import ModelMultipleChoiceField, inlineformset_factory, modelformset_factory
from django.shortcuts import redirect, render
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

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = models.WorkoutExercise
        fields = ('exercise', 'sets', 'reps_per_set')

    def __init__(self, *args, **kwargs):
        workout_id = kwargs.pop('workout_id', None)
        super(WorkoutExerciseForm, self).__init__(*args, **kwargs)
        if workout_id:
            self.fields['exercise'].queryset = models.Exercise.objects.filter(workoutexercise__workout_id=workout_id)




