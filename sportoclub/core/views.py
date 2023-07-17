from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Exercise, Workout, WorkoutExercise, SetLog, ExerciseCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkoutForm, WorkoutExerciseForm, SetLogForm, ExerciseSetLogForm
from django.forms import formset_factory
from django import forms
from django.db.models import Max, Avg
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.templatetags.static import static
from django.utils import timezone

def start_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    print(workout)
    first_exercise = WorkoutExercise.objects.filter(workout=workout).order_by('id').first()
    if first_exercise:
        return redirect('next_exercise', workout_pk=workout.pk, exercise_pk=first_exercise.pk)
    else:
        return render(request, 'workout_summary.html')  # or handle this case in some other way

def next_exercise(request, workout_pk, exercise_pk):
    workout = get_object_or_404(Workout, pk=workout_pk)
    current_exercise = get_object_or_404(WorkoutExercise, pk=exercise_pk)
    if request.method == "POST":
        form = ExerciseSetLogForm(request.POST, workout_exercise=current_exercise)
        if form.is_valid():
            # create SetLog objects like before
            for i in range(current_exercise.sets):
                setlog = SetLog.objects.create(
                    user=request.user,
                    workout_exercise=current_exercise,
                    weight=form.cleaned_data.get(f'weight_{i}'),
                    reps=form.cleaned_data.get(f'reps_{i}')
                )
                print(setlog)
            # then redirect to next exercise
            next_exercise = WorkoutExercise.objects.filter(workout=workout, id__gt=current_exercise.id).order_by('id').first()
            if next_exercise:
                return redirect('next_exercise', workout_pk=workout.pk, exercise_pk=next_exercise.pk)
            else:
                return redirect('workout_summary', workout_id=workout.pk)
    else:
        form = ExerciseSetLogForm(workout_exercise=current_exercise)
    return render(request, 'start_workout.html', {'form': form, 'workout': workout, 'workout_exercise': current_exercise})

def workout_summary(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    print(workout)
    now = timezone.now()
    start_time = now - timezone.timedelta(hours=1)
    exercise_logs = SetLog.objects.filter(workout_exercise__workout=workout, timestamp__gte=start_time).order_by('timestamp')
    
    # Create a dictionary where each key is an Exercise instance and each value is a list of SetLog instances
    exercises_data = {}
    for log in exercise_logs:
        if log.workout_exercise.exercise in exercises_data:
            exercises_data[log.workout_exercise.exercise].append(log)
        else:
            exercises_data[log.workout_exercise.exercise] = [log]
            
    # Calculate the average weight for each Exercise
    for exercise, logs in exercises_data.items():
        avg_weight = sum(log.weight for log in logs) / len(logs)
        exercises_data[exercise] = (logs, avg_weight)
    
    context = {
        'workout': workout,
        'exercises_data': exercises_data
    }
    return render(request, 'workout_summary.html', context)

def workout_charts(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    if not workout:
        return render(request, 'no_workouts.html')

    exercise_logs = SetLog.objects.filter(workout_exercise__workout=workout, user=request.user).order_by('timestamp')
    exercises_data = {}

    for log in exercise_logs:
        if log.workout_exercise.exercise in exercises_data:
            exercises_data[log.workout_exercise.exercise].append(log)
        else:
            exercises_data[log.workout_exercise.exercise] = [log]

    image_paths = []

    for exercise, logs in exercises_data.items():
        data = [log.weight for log in logs]
        dates = [log.timestamp.date() for log in logs]

        print(data)

        print(dates)

        plt.figure(figsize=(10, 6))
        sns.lineplot(x=dates, y=data)
        plt.title(exercise.name)
        
        # Save the figure to a .png image file
        image_filename = f"{exercise.name.replace(' ', '_')}_plot.png"
        image_filepath = os.path.join(settings.MEDIA_ROOT, 'images', image_filename)
        os.makedirs(os.path.dirname(image_filepath), exist_ok=True)
        plt.savefig(image_filepath)
        plt.close()


        # Store the static URL path to the image file
        image_url = settings.MEDIA_URL + 'images/' + image_filename
        image_paths.append(image_url)

    context = {
        'workout': workout,
        'image_paths': image_paths,
    }
    return render(request, 'workout_charts.html', context)

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

            # Create WorkoutExercise instances for each selected exercise
            for exercise in form.cleaned_data['exercises']:
                WorkoutExercise.objects.create(workout=workout, exercise=exercise, sets=0, reps_per_set=0)
            
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

@login_required
def add_sets_and_reps_to_workout(request, workout_id):
    WorkoutExerciseFormSet = formset_factory(WorkoutExerciseForm, extra=0)
    workout = get_object_or_404(Workout, id=workout_id)
    if request.method == 'POST':
        formset = WorkoutExerciseFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                workout_exercise_id = form.cleaned_data.get('id')
                if workout_exercise_id:
                    workout_exercise = get_object_or_404(WorkoutExercise, id=workout_exercise_id)
                    workout_exercise.sets = form.cleaned_data.get('sets')
                    workout_exercise.reps_per_set = form.cleaned_data.get('reps_per_set')
                    workout_exercise.save()
            return redirect('workout_detail', pk=workout.id)
    else:
        workout_exercises = workout.workoutexercises.exclude(exercise__isnull=True)
        initial_data = [{'id': workout_exercise.id, 'exercise': workout_exercise.exercise.id, 'sets': workout_exercise.sets, 'reps_per_set': workout_exercise.reps_per_set} for workout_exercise in workout_exercises]
        formset = WorkoutExerciseFormSet(initial=initial_data)

    return render(request, 'add_sets_and_reps_to_workout.html', {'formset': formset, 'workout': workout})