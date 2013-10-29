from itertools import chain
import datetime
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.shortcuts import render, redirect
from main.forms import LoginForm, StatusForm, MessageForm, SearchForm, EventForm
from main.middleware import send_message
from main.models import Message, Event
from registration.models import FingrUser, user_to_fingr


def index(request):
    context = {}

    if request.user.is_authenticated():
        user = user_to_fingr(request.user)
        context['authenticated'] = True
        context['userlist'] = FingrUser.objects.all()
        context['hasOnlineFriends'] = user.friends_list.filter(available=True).count

    return render(request, 'index.html', context)


def notify_all_friends(fingr_user, message_string):
    # send message to all friends
    for friend in fingr_user.friends_list:
        send_message(friend, fingr_user, message_string, Message.NOTIFICATION)


def notify_specific_friend(fingr_user, fingr_friend_pk, message_string):
    send_message(fingr_friend_pk, fingr_user, message_string, Message.NOTIFICATION)


def message_specific_friend(fingr_user, fingr_friend_pk, message_string):
    send_message(fingr_friend_pk, fingr_user, message_string, Message.MESSAGE)


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
                if user_to_fingr(user).verified:
                    notify_all_friends(fingr_user, 'Your friend ' + str(fingr_user.username) + ' has signed in')
                    # redirect to main page
                    return redirect('main.views.index')
                else:
                    django_logout(request)
                    #redirect to index page
                    return redirect('main.views.index')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def message(request, send_to_user):
    form = MessageForm()
    print (request.get_full_path(), send_to_user)
    context = {'valid': True, 'form': form}

    if request.user.is_authenticated():
        user = user_to_fingr(request.user)
        context['authenticated'] = True
        target_user = FingrUser.objects.filter(pk=send_to_user)
        if len(target_user) > 0:
            target_user = target_user[0]
        else:
            target_user = None

        if target_user:
            if request.POST:
                form = MessageForm(request.POST)
                if form.is_valid():
                    print 'Message Sent'
                    context['message_sent'] = True
                    message_specific_friend(user, target_user, form.cleaned_data['message'])
                else:
                    return redirect('main.views.message')

            if target_user in user.friends_list:
                pass
            else:
                if target_user == user:
                    context['feedback'] = 'Wow you must be lonely to send a message to yourself :('
                    context['valid'] = False

                else:
                    context['feedback'] = "You are sending a message to someone who isn't your friend. They may not get this message"

            received = user.messages_list.filter(sentFrom=target_user,type=Message.MESSAGE).order_by('-time')
            sent = target_user.messages_list.filter(sentTo=target_user, sentFrom=user, type=Message.MESSAGE).order_by('-time')

            user.messages_list.filter(sentTo=user, type=Message.MESSAGE).update(read=True)
            conversation_history = sorted(chain(sent, received), key=lambda instance: instance.time, reverse=True)

            #conversation_history = received

            #get the previous messages
            context['conversation'] = conversation_history[0:5]
            context['talking_to'] = target_user
        else:
            context['valid'] = False
            context['feedback'] = 'No such user exists'
    else:
        return redirect('main.views.login')
    return render(request, 'message.html', context)

@login_required
def set_online(request):
    user = user_to_fingr(request.user)
    user.automatic_availability = False
    user.available = True
    user.save()
    return redirect('main.views.index')


@login_required
def set_offline(request):
    user = user_to_fingr(request.user)
    user.automatic_availability = False
    user.available = False
    user.save()
    return redirect('main.views.index')

def set_automatic(request):
    user = user_to_fingr(request.user)
    user.automatic_availability = True
    user.save()
    return redirect('main.views.index')




def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('main.views.index')


@login_required
def add_friend(request, target_user_pk):
    """
    target_user_pk should be the primary key of the user that we want to add as a friend
    """

    user = user_to_fingr(request.user)
    target_user = FingrUser.objects.filter(pk=target_user_pk)[0]
    if target_user.username != request.user.username:
        user.friends.add(target_user)
        target_user.friends.add(user)


        notify_specific_friend(target_user, user, str(target_user.username) + ' has added you as a friend.')

    else:
        print "user tried to add themselves"
        # ignore a user trying to add themselves
    return redirect('main.views.index')


@login_required
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
        context['form'] = form

    return render(request, 'status.html', context)


@login_required
def inbox(request):
    context = {}
    if request.user.is_authenticated():
        context['authenticated'] = True

        user = user_to_fingr(request.user)
        conversations = user.messages_list.filter(type=Message.MESSAGE)


        people = set()
        for conversation in conversations:
            if conversation.sentFrom != user:
                people.add(conversation.sentFrom)

            if conversation.sentTo != user:
                people.add(conversation.sentTo)



        context['conversations'] = people
    else:
        return redirect('main.views.login')
    return render(request, 'inbox.html', context)


@login_required
def friends(request):
    context = {}
    if request.user.is_authenticated():
        context['authenticated'] = True
        context['userlist'] = FingrUser.objects.all()
    return render(request, 'available_friends.html', context)


@login_required
def search(request):
    context = {}
    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)
        context['authenticated'] = True
        # user is already searching
        if request.POST:
            form = SearchForm(request.POST)
            # display found users
            if form.is_valid():
                # all users
                unfiltered = (FingrUser.objects.filter(username__contains=form.cleaned_data['search']) | FingrUser.objects.filter(first_name__contains=form.cleaned_data['search']) | FingrUser.objects.filter(last_name__contains=form.cleaned_data['search']))
                # set(chain(...)) joins querysets and uniques them
                # http://stackoverflow.com/questions/431628/how-to-combine-2-or-more-querysets-in-a-django-view
                # users without extreme privacy
                visible = unfiltered.exclude(visibility="None")
                friends = {}
                for u in visible:
                    if (u.visibility=="Friends"):
                        friends = set(chain(friends, visible.filter(friends=f_user)))
                all = unfiltered.filter(visibility="All")
                context['userlist'] = set(chain(all, friends))
                return render(request, 'search.html', context)
            else:
                return render(request, 'search.html', context)
        else:
            context['userlist'] = FingrUser.objects.all()
            return render(request, 'search.html', context)
    return redirect('main.views.index')


@login_required
def events(request):
    context = {}
    user = user_to_fingr(request.user)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():

            currTime = datetime.datetime.now()

            good = True
            #we need to do some hacky stuff and set the year, because otherwise it might do 1889 which is an error
            startTime = form.cleaned_data['timeStart']
            endTime = form.cleaned_data['timeEnd']
            startTime = startTime.replace(year=currTime.year)
            endTime = endTime.replace(year=currTime.year)

            #HOW DO I VALIDATE PROPERLY?
            if endTime <= startTime:
                errors = form._errors.setdefault("timeEnd", ErrorList())
                errors.append(u"End time must be after Start time")
                good = False
            if form.cleaned_data['date'] < currTime.date():
                errors = form._errors.setdefault("date", ErrorList())
                errors.append(u"Day must be today or in the future")
                good = False

            if good:
                event = Event(title=form.cleaned_data['title'], owner=user, date=form.cleaned_data['date'],
                              timeStart=startTime, timeEnd=endTime, description=form.cleaned_data['description']
                )
                event.save()
                notify_all_friends(user, "You have been invited to " + user.full_name + "'s event: " + event.title)

    else:
        form = EventForm()

    context['form'] = form

    context['userEvents'] = Event.objects.filter(owner=user)
    context['friendEvents'] = Event.objects.filter(owner__in=user.friends_list)

    return render(request, 'events.html', context)


@login_required
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = user_to_fingr(request.user)
    if event.owner == user:
        event.delete()
    return redirect('main.views.events')


def activate(request):
    context = {}
    if FingrUser.objects.filter(username=request.GET.get('user')):
        fuser = FingrUser.objects.filter(username=request.GET.get('user'))[0]
        vcode = request.GET.get('code', '')
        if fuser.v_code == vcode:
            fuser.verify()
            fuser.save()
            print("activated")
            context['email'] = fuser
        else:
            context['code_fail'] = True
        return render(request, 'activate.html', context)
    else:
        context['user_fail'] = True
        return render(request, 'activate.html', context)
