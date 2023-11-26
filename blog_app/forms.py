from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=20, label=False)

    password_repeat = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'last_name', 'email', 'password', 'password_repeat']

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password == password_repeat:
            return password
        else:
            raise forms.ValidationError('Repetition of the password must be equal to the password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exists")
        else:
            return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=50, required=True)
