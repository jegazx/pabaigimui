from django.urls import path
from .views import ExerciseListView, ExerciseDetailView, ExerciseCreateView, ExerciseUpdateView, exercises_list
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercises/', exercises_list, name='exercises_list'),
    path('exercises/<int:pk>/', ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercises/new/', ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercises/<int:pk>/edit/', ExerciseUpdateView.as_view(), name='exercise_edit'),

]
