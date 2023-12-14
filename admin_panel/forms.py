from django import forms
from blog_app.models import *


class AddUserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=100)
    position = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3)))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'password',
            'profile', 'email'
        ]

    def clean(self):
        position = self.cleaned_data['position']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')

        if int(position) == 1:
            # Manager
            self.cleaned_data['is_superuser'], self.cleaned_data['is_staff'] = True, True
        elif int(position) == 2:
            # Admin
            self.cleaned_data['is_superuser'], self.cleaned_data['is_staff'] = False, True
        elif int(position) == 3:
            self.cleaned_data['is_superuser'], self.cleaned_data['is_staff'] = False, False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'body', 'thumbnail', 'category']

    def clean(self):
        return self.cleaned_data


class SearchForm(forms.Form):
    query = forms.CharField(max_length=10000)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text', 'description']