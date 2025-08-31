from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.contrib.auth.forms import UserCreationForm
from . models import Question , Answer , University, Program
from .forms import QuestionForm, AnswerForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from rest_framework.decorators import api_view
from django.conf import settings
import requests
import json
from openai import OpenAI
import os

from . import consumers

# Create your views here.



#openai api key 
DEEPSEEK_API_URL=os.getenv('DEEPSEEK_API_URL')
DEEPSEEK_API_KEY=os.getenv('DEEPSEEK_API_KEY')

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

@login_required
def universities_index(request):
    search = request.GET.get('s')
    if search:
        universities = University.objects.filter(name__icontains=search)
    else:
        universities = University.objects.all()
    return render(request, 'universities/index.html', { 'universities': universities , 'search': search, })

@login_required
def universities_detail(request, university_id):
    university = University.objects.get(id=university_id)

    level_filter = request.GET.get('level')

    # need it to show programs in uni
    programs = Program.objects.filter(university=university)

    if level_filter :
        programs = programs.filter(level=level_filter)

    levels = Program.objects.filter(university=university).values_list('level', flat=True).distinct()

    return render(request, 'universities/detail.html' , {'university': university, 'programs':programs,    'levels': levels,
        'selected_level': level_filter})


# Program
# if need the programs shown in another page not in uni
# def programs_index(request, university_id ):
#     university = University.objects.get(id=university_id)

#     programs = Program.objects.filter(university=university)
#     return render(request, 'universities/index.html', {'university': university, 'programs': programs })
@login_required
def programs_detail(request,university_id, program_id):
    program = Program.objects.get(id=program_id , university_id=university_id)
    questions = program.questions.all().prefetch_related("answers")

    q_form = QuestionForm()
    a_form = AnswerForm()

    if request.method == 'POST':
     
     if 'add_question' in request.POST:
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.user = request.user
            question.program = program
            question.save()
        return redirect('program_detail' ,university_id=university_id, program_id=program_id )
        

     elif 'edit_question' in request.POST:
            question_id = request.POST.get('question_id')
            question =Question.objects.get(id=question_id , user=request.user) 
            form = QuestionForm(request.POST , instance=question)
            if form.is_valid():
                form.save()
            return redirect('program_detail' , university_id=university_id, program_id=program_id) 

     elif 'add_answer' in request.POST:
            
            question_id = request.POST.get('question_id')
            question = Question.objects.get(id=question_id)
            a_form = AnswerForm(request.POST)
            if a_form.is_valid():
                answer = a_form.save(commit=False)
                answer.user = request.user
                answer.question = question
                answer.save()
                return redirect('program_detail' , university_id=university_id, program_id=program_id)  
            
            
    return render(request, 'programs/detail.html' ,  {
        "program": program,
        "questions": questions,
        "q_form": q_form,
        "a_form": a_form,
    })

@login_required
def question_delete(request, pk):
    question = Question.objects.get(id=pk, user=request.user)  # only owner
    program = question.program
    university_id = program.university.id
    program_id = program.id
    question.delete()
    return redirect("program_detail", university_id=university_id, program_id=program_id)

@login_required
def answer_delete(request, pk):
    answer = Answer.objects.get(id=pk, user=request.user)  # only owner
    program = answer.question.program
    university_id = program.university.id
    program_id = program.id
    answer.delete()
    return redirect("program_detail", university_id=university_id, program_id=program_id)

# favorite
@login_required
def favorite_program(request,university_id, program_id):
    program_check = Program.objects.filter(id=program_id)

    if program_check.exists():
        program = Program.objects.get(id=program_id)

        if request.user in program.users_favorited.all():
            program.users_favorited.remove(request.user)
        else:
            program.users_favorited.add(request.user)

        return redirect('detail', university_id=university_id)


@login_required    
def favorites_list(request):
    favorite_programs = Program.objects.filter(users_favorited=request.user).order_by('university__name')
    return render(request, 'myList.html', {'favorite_programs': favorite_programs})

@login_required
def edit_user(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user.username = username
        user.pasword = password
        user.save()

        return redirect('/')  
    return render(request, 'edit_user.html', {'user': user})

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


@login_required
def map_view(request):
    return render(request , 'map.html')

@login_required
def universities_geojson(request):
    features = []

    for uni in University.objects.all():
        if uni.latitude is None or uni.longitude is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(uni.longitude), float(uni.latitude)],
            },
            "properties": {
                "id": uni.id,
                "name": uni.name,
                "website": uni.website_link,
                "description": uni.description,
                "email": uni.email,
                "phone": uni.phone,
                "image_url": uni.image.url if uni.image else "",
            },
        })
    return   JsonResponse({"type": "FeatureCollection", "features": features})


# live chat 
@login_required
def live_chat(request):
    return render(request , 'live_chat.html' , {
        'username':request.user.username
    })

#CHAT AI FUNCTIONS
# @api_view(["POST"])
@login_required
@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return render(request , 'chat.html')
    
    data = json.loads(request.body)
    user_input = data["message"]

    print(user_input)
    
    if not user_input:
        return JsonResponse({"error": "Message is required"}, status=400)
    
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    data = {"prompt": user_input, "max_tokens": 150}
    
    # response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a university guidance chatbot that helps students pick their majors by asking questions"},
        {"role": "user", "content": user_input},
    ],
    stream=False
)
    print(response.choices[0].message.content)
    reply = response.choices[0].message.content
    # print(response)
    return JsonResponse({"response": reply})



