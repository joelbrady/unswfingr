from django.shortcuts import render
from registration.forms import RegistrationForm
from registration.models import create_fingr_user


def register(request):
    if request.POST:
        # load up the form with data from the POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = create_fingr_user(form.cleaned_data['email'], form.cleaned_data['password'])
            return render(request, 'register_result.html', {'email': user.username})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})