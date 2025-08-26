from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import University
# Create your views here.

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

def universities_index(request):
    universities = University.objects.all()
    return render(request, 'universities/index.html', { 'universities': universities })

def universities_detail(request, university_id):
    university = University.objects.get(id=university_id)
    return render(request, 'universities/detail.html' , {'university': university})

def signup(request):
    error_message = ""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('about')
        else:
            error_message = 'Invalid Signup - Try Again...'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)