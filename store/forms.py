from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)


class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 
        'password2','email']

class UpdateUserInfo(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email']
    

