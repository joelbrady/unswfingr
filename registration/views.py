from django.shortcuts import render
from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return render(request, 'register_result.html', form.cleaned_data)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})