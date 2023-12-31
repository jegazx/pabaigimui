from django.urls import path
from .views import  ExerciseDetailView, ExerciseCreateView, ExerciseUpdateView, exercises_list, WorkoutDetailView, WorkoutListView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('exercises/', exercises_list, name='exercises_list'),
    path('exercises/<int:pk>/', ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercises/new/', ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercises/<int:pk>/edit/', ExerciseUpdateView.as_view(), name='exercise_edit'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
    path('workout/new/', views.create_workout, name='create_workout'),
    path('workouts/', WorkoutListView.as_view(), name='workout_list'),
    path('workout/<int:workout_id>/add_sets_reps/', views.add_sets_and_reps_to_workout, name='add_sets_and_reps_to_workout'),
    path('workout/<int:pk>/start/', views.start_workout, name='start_workout'),
    path('workout/<int:workout_id>/summary/', views.workout_summary, name='workout_summary'),
    path('workout/<int:workout_pk>/exercise/<int:exercise_pk>', views.next_exercise, name='next_exercise'),
    path('workouts/<int:workout_id>/charts/', views.workout_charts, name='workout_charts'),
]