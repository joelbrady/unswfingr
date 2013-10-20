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

            numUnreadMessages = user.messages_list.filter(type=Message.MESSAGE, read=False).count()
            if (numUnreadMessages > 0):
                messages.info(request, str(numUnreadMessages) + ' new unread message(s)')
            for message in user.messages_list:

                if (message.type == Message.NOTIFICATION):
                    messages.success(request, message.text)
                    message.delete()
                else:
                    if not message.read:
                        messages.success(request, str(message.sentFrom) + ' sent you a message.')
                        message.read=True
                        message.save()
                    #messages.success(request, 'You have a new message from' + str(message.sentFrom))




def send_message(messageTo, messageFrom, messageText, typeOfMessage):
    """
    This function allows you to send a notification to a particular user. Must specify a FingrUser to, from, as well as the message itself.

    In the future we will probably need to add a type of message such as alert, or something like that
    """
    userTo = FingrUser.objects.filter(username=messageTo)[0]
    message = Message(text=messageText, sentFrom=messageFrom, type=typeOfMessage)
    message.save()
    userTo.save()
    userTo.messages.add(message)
