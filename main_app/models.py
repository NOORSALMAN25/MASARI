from django.db import models
from django.urls import reverse
from datetime import date #23
from django.contrib.auth.models import User


# Create your models here.



class University(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website_link = models.URLField(max_length=300, blank=True)
    description = models.TextField(max_length=300, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='universities/', blank=True, null=True)


    def __str__(self):
        return self.name
    

class Program(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    duration = models.IntegerField()
    language = models.CharField(max_length=100)
    requirements = models.TextField()
    resources_link = models.TextField(max_length=300)

    # 1-M uni-pro
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    # M-M 
    users_favorited = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)


class Question(models.Model):
    question_txt = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    program = models.ForeignKey(Program , on_delete=models.CASCADE , related_name="questions" )

    def __str__(self):
        return self.question_txt

class Answer(models.Model):
    answer_txt = models.CharField(max_length=200)    
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    question = models.ForeignKey(Question , on_delete=models.CASCADE , related_name='answers')

    def __str__(self):
        return self.answer_txt
    
