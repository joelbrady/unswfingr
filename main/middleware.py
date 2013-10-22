from django.contrib import messages
from main.models import Message
from registration.models import user_to_fingr


class CheckMessagesMiddleware(object):
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            user = user_to_fingr(request.user)
            if user is not None:
                num_unread_messages = user.messages_list.filter(type=Message.MESSAGE, read=False).count()
                if num_unread_messages > 0:
                    messages.info(request, str(num_unread_messages) + ' new unread message(s)')
                for message in user.messages_list:
                    if message.type == Message.NOTIFICATION:
                        messages.success(request, message.text)
                        message.delete()
                    else:
                        if not message.read:
                            messages.success(request, str(message.sentFrom) + ' sent you a message.')
                            message.read=True
                            message.save()
                        #messages.success(request, 'You have a new message from' + str(message.sentFrom))


def send_message(message_to, message_from, message_text, type_of_message):
    """
    This function allows you to send a notification to a particular user. Must specify a FingrUser to, from, as well as the message itself.

    In the future we will probably need to add a type of message such as alert, or something like that
    """
    user_to = message_to
    message = Message(text=message_text, sentFrom=message_from, type=type_of_message)
    message.save()
    user_to.save()
    user_to.messages.add(message)
