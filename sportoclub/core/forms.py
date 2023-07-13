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
    exercises = forms.ModelMultipleChoiceField(
        queryset=models.Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'exercise-checkbox'})
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



# class WorkoutExerciseForm(forms.ModelForm):
#     class Meta:
#         model = models.WorkoutExercise
#         fields = ('exercise', 'sets', 'reps_per_set')

#     def __init__(self, *args, **kwargs):
#         workout_id = kwargs.pop('workout_id', None)
#         super(WorkoutExerciseForm, self).__init__(*args, **kwargs)
#         if workout_id:
#             workout = models.Workout.objects.get(id=workout_id)
#             self.fields['exercise'].queryset = workout.exercises.all()
# veikiantis

class WorkoutExerciseForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    sets = forms.IntegerField(min_value=0)
    reps_per_set = forms.IntegerField(min_value=0)

    class Meta:
        model = models.WorkoutExercise
        fields = ['id', 'sets', 'reps_per_set', 'exercise']

    def __init__(self, *args, **kwargs):
            super(WorkoutExerciseForm, self).__init__(*args, **kwargs)
            if self.instance and hasattr(self.instance, 'exercise'):
                self.initial['exercise'] = self.instance.exercise.name


class SetLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        workout = kwargs.pop('workout', None)
        sets = kwargs.pop('sets', 1)
        super(SetLogForm, self).__init__(*args, **kwargs)
        if workout:
            self.fields['workout_exercise'].queryset = models.WorkoutExercise.objects.filter(workout=workout)
            self.sets = sets

    class Meta:
        model = models.SetLog
        fields = ('weight', 'reps')

class ExerciseSetLogForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.workout_exercise = kwargs.pop('workout_exercise')
        super().__init__(*args, **kwargs)
        self.sets = self.workout_exercise.sets
        for i in range(self.sets):
            self.fields[f'weight_{i}'] = forms.FloatField()
            self.fields[f'reps_{i}'] = forms.IntegerField()
