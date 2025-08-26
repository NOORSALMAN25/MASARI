from django.db import models
from django.urls import reverse
from datetime import date #23
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_txt = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    # program = models.ForeignKey()

class Answer(models.Model):
    answer_txt = models.CharField(max_length=200)    
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    question = models.ForeignKey(Question , on_delete=models.CASCADE , related_name='answers')
    



