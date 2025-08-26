from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website_link = models.CharField(max_length=300)
    description = models.TextField(max_length=300)
    email = models.TextField(max_length=50)
    phone = models.IntegerField()
    image = models.ImageField(upload_to='main_app/static/uploads/', default='')

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
