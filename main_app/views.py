from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.contrib.auth.forms import UserCreationForm
from . models import Question , Answer , University, Program
from .forms import QuestionForm, AnswerForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from django.conf import settings


# Create your views here.

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

def universities_index(request):
    search = request.GET.get('s')
    if search:
        universities = University.objects.filter(name__icontains=search)
    else:
        universities = University.objects.all()
    return render(request, 'universities/index.html', { 'universities': universities , 'search': search, })

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


def question_delete(request, pk):
    question = Question.objects.get(id=pk, user=request.user)  # only owner
    program = question.program
    university_id = program.university.id
    program_id = program.id
    question.delete()
    return redirect("program_detail", university_id=university_id, program_id=program_id)


def answer_delete(request, pk):
    answer = Answer.objects.get(id=pk, user=request.user)  # only owner
    program = answer.question.program
    university_id = program.university.id
    program_id = program.id
    answer.delete()
    return redirect("program_detail", university_id=university_id, program_id=program_id)

# favorite
def favorite_program(request,university_id, program_id):
    program_check = Program.objects.filter(id=program_id)

    if program_check.exists():
        program = Program.objects.get(id=program_id)

        if request.user in program.users_favorited.all():
            program.users_favorited.remove(request.user)
        else:
            program.users_favorited.add(request.user)

        return redirect('detail', university_id=university_id)

    
def favorites_list(request):
    favorite_programs = Program.objects.filter(users_favorited=request.user).order_by('university__name')
    return render(request, 'myList.html', {'favorite_programs': favorite_programs})

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


def map_view(request):
    return render(request , 'map.html')

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

#CHAT AI FUNCTIONS

def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': "You are a helpful assistant"},
                {'role': 'user', 'content': user_message},
            ],
            max_token=150
        )
        ai_message = response.choices[0].message.content
        return JsonResponse({'message': ai_message})
    return render(request, 'chat.html')