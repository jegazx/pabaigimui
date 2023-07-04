from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Exercise, Workout, WorkoutExercise, SetLog, ExerciseCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    if request.user.is_authenticated:  
        # User is logged in
        return render(request, 'index_authenticated.html')
    else:
        # User is not logged in
        return render(request, 'index.html')
    
from django.shortcuts import render
from .models import Exercise, ExerciseCategory

from django.shortcuts import render
from .models import Exercise, ExerciseCategory

def exercises_list(request):
    categories = ExerciseCategory.objects.all()
    exercises = Exercise.objects.none()  # start with no exercises
    
    category_id = request.GET.get('category')
    if category_id:
        exercises = Exercise.objects.filter(category_id=category_id)  # only get exercises if a category is selected

    return render(request, 'exercises_list.html', {'exercises': exercises, 'categories': categories, 'current_category_id': category_id})

def get_embed_url(self):
    video_id = self.video_url.split('/')[-1] # splits on slash and takes the last piece
    print(video_id)
    return f"https://www.youtube.com/embed/{video_id}"


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
    fields = ('name', 'video_url', 'category') 
    template_name = 'exercise_form.html'

class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    fields = ('name', 'video_url', 'category')
    template_name = 'exercise_form.html'

