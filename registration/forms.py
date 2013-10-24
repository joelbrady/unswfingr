from django import forms
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH
from django.forms import ModelForm
from registration.models import FingrUser


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)
    
    # django automatically calls clean_ for each vield in the form
    # either return the cleaned value, or raise a forms.ValidationError
    def clean_password2(self):
        # idea found in built in django forms
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password

class FingrUserForm(ModelForm):
    class Meta:
        model = FingrUser
        exclude = ('messages','verified','django_user', 'friends', 'v_code', 'available', 'static_locations')
