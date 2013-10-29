from django.contrib import messages
from main.models import Message
from registration.models import user_to_fingr
from profile.views import automatic_is_available


class CheckAutomaticAvailability(object):
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        assert hasattr(request,
                       'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if(request.user.is_authenticated()):
            user = user_to_fingr(request.user)
            if user is not None:
                if(user.automatic_availability == True):
                    automatic_is_available(request)



class CheckMessagesMiddleware(object):
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        assert hasattr(request,
                       'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            user = user_to_fingr(request.user)

            if user is not None:
                num_unread_messages = user.messages_list.filter(type=Message.MESSAGE, read=False).exclude(sentFrom=user).count()
                if num_unread_messages > 0:
                    messages.success(request, "<a href='/inbox'>"+str(num_unread_messages) + ' new unread message(s)</a>',extra_tags='safe')
                for message in user.messages_list:
                    if message.type == Message.NOTIFICATION:
                        messages.success(request, message.text)
                        message.delete()


def send_message(message_to, message_from, message_text, type_of_message):
    """
    This function allows you to send a notification to a particular user. Must specify a FingrUser to, from, as well as the message itself.

    In the future we will probably need to add a type of message such as alert, or something like that
    """
    user_to = message_to
    message = Message(text=message_text, sentFrom=message_from, type=type_of_message, sentTo=user_to)
    message.save()
    user_to.save()
    user_to.messages.add(message)

    message_from.save()
    message_from.messages.add(message)


def fingr_user_everywhere(request):
    dictionary = {}
    if request.user:
        if request.user.is_authenticated():
            user = user_to_fingr(request.user)
            if user is not None:
                dictionary['fingr_user'] = user

                for message in user.messages_list:
                    if message.type == Message.MESSAGE and message.read == False and message.sentTo == user:
                        dictionary['newMessage'] = True



    return dictionary