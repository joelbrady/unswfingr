from itertools import chain
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
from main.forms import LoginForm, StatusForm, MessageForm
from main.middleware import send_message
from main.models import Message
from registration.models import FingrUser, user_to_fingr
from django.contrib import messages

def index(request):
    context = {}

    if request.user.is_authenticated():
        context['authenticated'] = True
        context['userlist'] = FingrUser.objects.all()
        user = user_to_fingr(request.user)
        context['user'] = user

    return render(request, 'index.html', context)


def notify_all_friends(fingr_user, messageString):
    # send message to all friends
    for friend in fingr_user.friends_list:
        send_message(friend.username, fingr_user.username, messageString, Message.NOTIFICATION)

def notify_specific_friend(fingr_user, fingr_friend, messageString):
    send_message(fingr_friend.username, fingr_user.username, messageString, Message.NOTIFICATION)


def message_specific_friend(fingr_user, fingr_friend, messageString):
    send_message(fingr_friend.username, fingr_user.username, messageString,Message.MESSAGE)




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
                fingr_user = user_to_fingr(request.user)
                notify_all_friends(fingr_user, 'Your friend ' + str(fingr_user.username) + ' has signed in')

                # redirect to main page
                return redirect('main.views.index')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def message(request, send_to_user):
    form = MessageForm()
    print (request.get_full_path(), send_to_user)
    context = {}


    context['valid'] = True
    context['form'] = form

    if request.user.is_authenticated():
        user = user_to_fingr(request.user)
        context['authenticated'] = True


        if int(send_to_user) <= FingrUser.objects.count():
            target_user = FingrUser.objects.filter(pk=send_to_user)[0]

            if target_user in user.friends_list:
                pass
            else:
                if target_user == user:
                    context['feedback'] = 'Wow you must be lonely to send a message to yourself :('
                    context['valid'] = False

                else:
                    context['feedback'] = "You are sending a message to someone who isn't your friend. They may not get this message"

            received = user.messages_list.filter(sentFrom=target_user, type=Message.MESSAGE).order_by('-time')
            sent = target_user.messages_list.filter(sentFrom=user, type=Message.MESSAGE).order_by('-time')

            user.messages_list.filter(sentFrom=target_user, type=Message.MESSAGE).update(read=True)


            conversation_history = sorted(chain(sent,received), key=lambda instance: instance.time, reverse=True)

            #get the previous messages
            context['conversation'] = conversation_history[0:5]
            context['talking_to'] = target_user
            context['user'] = user


            if request.POST:
                form = MessageForm(request.POST)
                if form.is_valid():
                    print 'Message Sent'
                    context['message_sent'] = True
                    message_specific_friend(user, target_user, form.cleaned_data['message'])
                    form = MessageForm()

                else:
                    return redirect('main.views.message')
        else:
            context['valid'] = False
            context['feedback'] = 'No such user exists'



    else :
        return redirect('main.views.login')


    return render(request, 'message.html', context)



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
        notify_specific_friend(target_user, user, str(target_user.username) + 'has added you as a friend.')

    else:
        print "user tried to add themselves"
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

                #only notify them if its actually changed
                if not user.available:
                    notify_all_friends(user, 'Your friend ' + str(user.username) + ' is now FREE')

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


def view_map(request):
    return render(request, 'map.html')

