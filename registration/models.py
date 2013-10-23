from django.contrib.auth.models import User
from django.db import models
from main.models import Message




class FingrUser(models.Model):
    """
    This is our user class that has our custom info
    we will use the built in django user for authentication
    the username is the email address, they can be used
    interchangabily.
    """

    django_user = models.ForeignKey(User, unique=True)
    username = models.EmailField(max_length=100)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    friends = models.ManyToManyField('self')
    verified = models.BooleanField(default=False)
    v_code = models.CharField(max_length=50)
    available = models.BooleanField(default=False)
    messages = models.ManyToManyField(Message)



    def _get_username(self):
        return self.django_user.username

    def _get_email(self):
        return self.django_user.email

    def _friends_list(self):
        return self.friends.all()

    def _messages_list(self):
        return self.messages.all()
    friends_list = property(_friends_list)

    messages_list = property(_messages_list)

    def __unicode__(self):
        return self.username

    def verify(self):
        self.verified = True


def user_to_fingr(django_user):
    """
    Converts a django auth User object to a FingrUser object
    """
    found_users = FingrUser.objects.filter(django_user=django_user)
    # a django User should map to exactly one FingrUser
    assert len(found_users) <= 1
    if len(found_users) == 1:
        return found_users[0]
    else:
        return None


def create_fingr_user(email, password, **kwargs):
    """
    This function takes clean data to create a fingr user,
    please do not create one yourself
    """

    # the django create_user method automatically saves it in the database for us
    django_user = User.objects.create_user(username=email, email=email, password=password)

    fingr_user = FingrUser(django_user=django_user, username=email, email=email, **kwargs)
    fingr_user.save()


    return fingr_user