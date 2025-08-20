from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    class Meta:
        model = get_user_model
        fields = ('username','email', 'password1', 'password2')