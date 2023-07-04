from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Exercise

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # User is logged in
        return render(request, 'index_authenticated.html')
    else:
        # User is not logged in
        return render(request, 'index.html')
    

class ExerciseListView(ListView):
    model = Exercise
    template_name = 'exercise_list.html'

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'exercise_detail.html'

class ExerciseCreateView(CreateView):
    model = Exercise
    fields = ('name', 'video_url',) 
    template_name = 'exercise_form.html'

class ExerciseUpdateView(UpdateView):
    model = Exercise
    fields = ('name', 'video_url',)
    template_name = 'exercise_form.html'
