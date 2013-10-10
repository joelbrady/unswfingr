from django import forms
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)
