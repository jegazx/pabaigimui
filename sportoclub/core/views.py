from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Exercise, Workout, WorkoutExercise, SetLog, ExerciseCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkoutForm

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
            form.save_m2m()
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm()
    
    return render(request, 'create_workout.html', {'form': form})

class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout_detail.html'
    
class WorkoutListView(ListView):
    model = Workout
    template_name = 'core/workout_list.html'  # adjust this to match your actual template

