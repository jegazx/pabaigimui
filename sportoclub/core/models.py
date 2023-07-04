from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Exercise  Categories"

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    video_url = models.URLField()
    category = models.ForeignKey(ExerciseCategory, on_delete=models.SET_NULL, null=True, related_name="exercises")

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exercise_detail", kwargs={"pk": self.pk})

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    exercises = models.ManyToManyField(Exercise, related_name="WorkoutExercises")

    class Meta:
        verbose_name = _("workout")
        verbose_name_plural = _("workouts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("workout_detail", kwargs={"pk": self.pk})
    
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps_per_set = models.PositiveIntegerField()  

    class Meta:
        verbose_name = _("workoutexercise")
        verbose_name_plural = _("workoutexercises")

    def __str__(self):
        return self.exercise.name

    def get_absolute_url(self):
        return reverse("workoutexercise_detail", kwargs={"pk": self.pk})

class SetLog(models.Model):
    workou_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    weight = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    

    class Meta:
        verbose_name = _("setlog")
        verbose_name_plural = _("setlogs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("setlog_detail", kwargs={"pk": self.pk})
