from django.shortcuts import render
from django.contrib.auth.models import User
from registration.forms import RegistrationForm


def register(request):
    if request.POST:
        # load up the form with data from the POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            return render(request, 'register_result.html', {'email': user.username})
        else:
            print form.errors
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})