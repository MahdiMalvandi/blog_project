from django import forms
from blog_app.models import *
from django.contrib.auth.models import Permission


class AddUserForm(forms.ModelForm):
    position = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3)))
    password = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'password',
            'profile', 'email', 'job'
        ]

    exclude = ('password',)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.exclude(pk=self.instance.pk).filter(
            username__iexact=username
        ).exists()

        if users:
            raise forms.ValidationError("Username has already taken by someone else")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.exclude(pk=self.instance.pk).filter(
            email__iexact=email
        ).exists()

        if users:
            raise forms.ValidationError("Email has already taken by someone else")

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == '' and self.instance.pk:
            return self.instance.password
        elif password != '' and self.instance.pk:
            return password
        elif password == '' and not self.instance.pk:
            return forms.ValidationError('Password Must not to be empty')
        else:
            return password

    def clean(self):

        position = self.cleaned_data['position']

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
        password = self.cleaned_data['password']
        user = super().save(commit=False)
        if not password and self.instance.pk:
            # If password is not provided and user exists, keep the previous password
            if commit:
                user.save()
            return user
        else:
            # If password provided or it's a new user, return the entered password
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user


class AddBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=100)

    class Meta:
        model = Post
        fields = ['title', 'description', 'body', 'thumbnail', 'category']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=10000)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text', 'description']


# forms.py


class UserPermissionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UserPermissionForm, self).__init__(*args, **kwargs)
        user_permissions = user.get_user_permissions()
        all_permissions = Permission.objects.all()
        bad_permissions = ['ticket', 'session', 'dialog', 'content type', 'log entry', 'group']
        for permission in all_permissions:

            if permission.content_type.name not in bad_permissions:
                checkbox_initial = f'{permission.content_type.app_label}.{permission.codename}' in user_permissions

                self.fields['permission_{}'.format(permission.id)] = forms.BooleanField(
                    label=permission.name,
                    initial=checkbox_initial,
                    required=False)
