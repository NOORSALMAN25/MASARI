from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website_link = models.CharField(max_length=300)
    description = models.TextField(max_length=300)
    email = models.TextField(max_length=50)
    phone = models.IntegerField(max_length=15)
    image = models.ImageField(upload_to='main_app/static/uploads/', default='')