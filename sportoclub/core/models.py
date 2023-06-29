from django.db import models
from django.urls import reverse

class Exercise(models.Model):

    

    class Meta:
        verbose_name = _("exercise")
        verbose_name_plural = _("exercises")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exercise_detail", kwargs={"pk": self.pk})

