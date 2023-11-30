from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'username', 'last_name', 'email', 'password1', 'password2']



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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63)


class AddPostForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'body', 'thumbnail', 'category']
        model = Post


class SearchPostForm(forms.Form):
    q = forms.CharField(max_length=1000)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'body', 'reply', 'point']


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'job', 'bio', 'profile', 'email']
