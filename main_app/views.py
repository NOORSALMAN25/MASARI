from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import University, Program
# Create your views here.


# Create your views here.
# @login_required(login_url='login')
def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

def universities_index(request):
    universities = University.objects.all()
    return render(request, 'universities/index.html', { 'universities': universities })

def universities_detail(request, university_id):
    university = University.objects.get(id=university_id)

    # need it to show programs in uni
    programs = Program.objects.filter(university=university)

    return render(request, 'universities/detail.html' , {'university': university, 'programs':programs})


# Program
# if need the programs shown in another page not in uni
# def programs_index(request, university_id ):
#     university = University.objects.get(id=university_id)

#     programs = Program.objects.filter(university=university)
#     return render(request, 'universities/index.html', {'university': university, 'programs': programs })

def programs_detail(request,university_id, program_id):
    program = Program.objects.get(id=program_id , university_id=university_id)
    return render(request, 'programs/detail.html' , {'program': program})

def signup(request):
    error_message = ""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Signup - Try Again...'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)