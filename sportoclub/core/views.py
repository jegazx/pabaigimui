from django.shortcuts import render

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # User is logged in
        return render(request, 'index_authenticated.html')
    else:
        # User is not logged in
        return render(request, 'index.html')