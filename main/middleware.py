from django.contrib import messages
from django.utils import timezone
from main.models import Message

from registration.models import user_to_fingr, FingrUser

# This
class checkMessagesMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            user = user_to_fingr(request.user)

            if (user.messages_list.count() > 0):
                messages.info(request, str(user.messages_list.count()) + ' message(s)')
                for message in user.messages_list:
                    messages.success(request, message.text)
                    message.delete()




def send_message(messageTo, messageFrom, messageText):
    """
    This function allows you to send a notification to a particular user. Must specify a FingrUser to, from, as well as the message itself.

    In the future we will probably need to add a type of message such as alert, or something like that
    """
    userTo = FingrUser.objects.filter(username=messageTo)[0]
    message = Message(text=messageText, sentFrom=messageFrom)
    message.save()
    userTo.save()
    userTo.messages.add(message)
