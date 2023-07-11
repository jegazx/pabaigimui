from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Exercise, Workout, WorkoutExercise, SetLog, ExerciseCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkoutForm, WorkoutExerciseForm
from django.forms import formset_factory
from django import forms


WorkoutExerciseFormSet = formset_factory(WorkoutExerciseForm, extra=1)


# Create your views here.
def index(request):
    if request.user.is_authenticated:  
        # User is logged in
        return render(request, 'index_authenticated.html')
    else:
        # User is not logged in
        return render(request, 'index.html')

def exercises_list(request):
    categories = ExerciseCategory.objects.all()
    exercises = Exercise.objects.none()  # start with no exercises
    
    category_id = request.GET.get('category')
    if category_id:
        exercises = Exercise.objects.filter(category_id=category_id)  # only get exercises if a category is selected

    return render(request, 'exercises_list.html', {'exercises': exercises, 'categories': categories, 'current_category_id': category_id})

# def get_embed_url(self):
#     video_id = self.video_embed.split('/')[-1] # splits on slash and takes the last piece
#     return video_id


def exercise_detail(request, pk: int):
    ex = Exercise.objects.get(pk=pk)
    return render(request, 'exercise_detail.html', {'exercise': ex})

class ExerciseListView(ListView):
    model = Exercise
    template_name = 'exercise_list.html'

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'exercise_detail.html'

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    fields = ('name', 'video_embed', 'category') 
    template_name = 'exercise_form.html'

class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    fields = ('name', 'video_embed', 'category')
    template_name = 'exercise_form.html'

@login_required
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            workout.exercises.set(form.cleaned_data['exercises'])
            return redirect('add_sets_and_reps_to_workout', workout_id=workout.id)
    else:
        form = WorkoutForm()

    return render(request, 'create_workout.html', {'form': form})

class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout_detail.html'
    
class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workout_list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

# @login_required
# def add_sets_and_reps_to_workout(request, workout_id):
#     WorkoutExerciseFormSet = formset_factory(WorkoutExerciseForm, extra=0)
#     workout = get_object_or_404(Workout, id=workout_id)
#     if request.method == 'POST':
#         formset = WorkoutExerciseFormSet(request.POST, form_kwargs={'workout_id': workout.id})
#         if formset.is_valid():
#             for form in formset:
#                 workout_exercise = form.save(commit=False)
#                 workout_exercise.workout = workout
#                 workout_exercise.save()
#             return redirect('workout_detail', pk=workout.id)
#     else:
#         initial_data = [{'exercise': exercise.id} for exercise in workout.exercises.all()]
#         formset = WorkoutExerciseFormSet(initial=initial_data, form_kwargs={'workout_id': workout.id})

#     return render(request, 'add_sets_and_reps_to_workout.html', {'formset': formset, 'workout': workout})
# veikiantis

@login_required
def add_sets_and_reps_to_workout(request, workout_id):
    WorkoutExerciseFormSet = formset_factory(WorkoutExerciseForm, extra=0)
    workout = get_object_or_404(Workout, id=workout_id)
    if request.method == 'POST':
        formset = WorkoutExerciseFormSet(request.POST, form_kwargs={'workout_id': workout.id})
        if formset.is_valid():
            for form in formset:
                workout_exercise = form.save(commit=False)
                workout_exercise.workout = workout
                workout_exercise.save()
            return redirect('workout_detail', pk=workout.id)
    else:
        initial_data = [{'exercise': exercise.id} for exercise in workout.exercises.all()]
        formset = WorkoutExerciseFormSet(initial=initial_data, form_kwargs={'workout_id': workout.id})

    return render(request, 'add_sets_and_reps_to_workout.html', {'formset': formset, 'workout': workout})
