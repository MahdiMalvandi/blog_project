import ckeditor_uploader
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

    def clean(self):
        cleaned_data = self.cleaned_data

        username = cleaned_data['username']
        password = cleaned_data['password']

        # username clean
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist")

        # password clean
        if user.check_password(password):
            return cleaned_data
        else:
            raise forms.ValidationError("Password does not match")


class AddPostForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'body', 'thumbnail', 'category', 'description']
        model = Post


class SearchPostForm(forms.Form):
    q = forms.CharField(max_length=1000)


class AddCommentForm(forms.ModelForm):
    point_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    point = forms.ChoiceField(choices=point_choices, required=False)

    class Meta:
        model = Comment
        fields = ['body', 'reply', 'point']


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'job', 'bio', 'profile', 'email']


class AccountChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100)
    user = forms.IntegerField()

    def clean(self):

        user_id = self.cleaned_data['user']
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        user = User.objects.get(id=user_id)

        if user.check_password(old_password):
            return self.cleaned_data
        else:
            raise forms.ValidationError('Your Password in wrong')
