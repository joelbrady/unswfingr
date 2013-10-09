from django import forms
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=MAXIMUM_PASSWORD_LENGTH)
