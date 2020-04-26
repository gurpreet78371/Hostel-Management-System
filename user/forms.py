from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, complaint
import datetime

num = int(str(datetime.datetime.now().year)[:2] + str(101000))


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['StudentID', 'Branch', 'YearOfStudy', 'ContactNumber', ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', ]


class complaintForm(forms.ModelForm):
    class Meta:
        model = complaint
        fields = ['category', 'title', 'content', 'image', ]
