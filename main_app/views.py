from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.contrib.auth.forms import UserCreationForm
from . models import Question , Answer
from django.contrib.auth import login

# Create your views here.

class QuestionCreate(CreateView):
    model = Question
    fields = ['question_txt' , 'date_posted']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class QuestionUpdate(UpdateView):
    model = Question
    fields=[ 'question_txt']  

class QuestionDelete(DeleteView):
    model = Question
    success_url = '/'     





def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

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