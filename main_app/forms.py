from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100,
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class Meta:
    model = User
    fields = ['username', 'password']