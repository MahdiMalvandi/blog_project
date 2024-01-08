from django import forms
from django.contrib.auth import authenticate
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

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username Already Exists")
        else:
            return username


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            user = None
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    pass
            else:
                user = authenticate(username=username_or_email, password=password)

            if user is None or not user.check_password(password):
                raise forms.ValidationError("Invalid username/email or password")

        return cleaned_data


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

    def clean_username(self):
        new_username = self.cleaned_data['username']
        old_username = self.instance.username

        if new_username != old_username:
            if User.objects.filter(username=new_username).exists():
                raise forms.ValidationError('The username already exists')
        return new_username

    def clean_email(self):
        new_email = self.cleaned_data['email']
        old_email = self.instance.email

        if new_email != old_email:
            if User.objects.filter(email=new_email).exists():
                raise forms.ValidationError('The email already exists')
        return new_email


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


class AddNewMessageForm(forms.Form):
    type_of_tickets = (
        ('Bug', 'Bug'),
        ('Proposal', 'Proposal'),
        ('Support', 'Support'),
        ('Criticism', 'Criticism'),
    )
    body = forms.CharField(max_length=100000)
    title = forms.CharField(max_length=10000)
    type = forms.ChoiceField(choices=type_of_tickets)


class AnswerForm(forms.Form):
    body = forms.CharField(max_length=100000)
