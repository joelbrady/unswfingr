from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from main.forms import LoginForm


def index(request):
    context = {}
    if request.user.is_authenticated():
        context['authenticated'] = True
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated():
        redirect('main.views.index')
    if request.POST:
        # load up the form with data from the POST request
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                # redirect to main page
                return redirect('main.views.index')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('main.views.index')