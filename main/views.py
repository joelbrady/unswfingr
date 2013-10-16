from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from main.forms import LoginForm, StatusForm
from registration.models import FingrUser, user_to_fingr


def index(request):
    context = {}
    if request.user.is_authenticated():
        context['authenticated'] = True
        context['userlist'] = FingrUser.objects.all()
        context['user'] = user_to_fingr(request.user)
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated():
        return redirect('main.views.index')
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


def add_friend(request, target_user_pk):
    """
    target_user_pk should be the primary key of the user that we want to add as a friend
    """
    user = user_to_fingr(request.user)
    target_user = FingrUser.objects.filter(pk=target_user_pk)[0]
    if target_user.username != request.user.username:
        user.friends.add(target_user)
        target_user.friends.add(user)
    # ignore a user trying to add themselves
    return redirect('main.views.index')


def set_status(request):
    context = {}

    if request.POST:
        form = StatusForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['available']
            user = user_to_fingr(request.user)
            if choice == 'ON':
                user.available = True
            else:
                user.available = False
            user.save()
    else:
        form = StatusForm()

    if request.user.is_authenticated():
        context['authenticated'] = True
        context['user'] = user_to_fingr(request.user)
        context['form'] = form

    return render(request, 'status.html', context)


def friends(request):
    context = {}
    if request.user.is_authenticated():
        context['authenticated'] = True
        context['userlist'] = FingrUser.objects.all()
        context['user'] = user_to_fingr(request.user)
    return render(request, 'available_friends.html', context)