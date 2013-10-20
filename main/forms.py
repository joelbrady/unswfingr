from django import forms
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)


class StatusForm(forms.Form):
    STATUS_CHOICES = (('ON', 'Available'),
                      ('OFF', 'Not Free'))
    available = forms.ChoiceField(choices=STATUS_CHOICES)

    #amount = forms.IntegerField(min_value=5, max_value=120)
    

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)
    
class ActivateForm(forms.Form):
    activate = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
