from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }))
    
    password1: forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'
            }))
    
    password2: forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'
            }))
    
    class Meta:
        model = User
        fields = ('username','phone_number','meter_number','password1','password2')