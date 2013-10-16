from django.contrib.auth.models import User
from django.db import models


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

    available = models.BooleanField(default=False)


    def _get_username(self):
        return self.django_user.username

    def _get_email(self):
        return self.django_user.email

    def _friends_list(self):
        return self.friends.all()

    friends_list = property(_friends_list)

    def __unicode__(self):
        return self.username


def user_to_fingr(django_user):
    """
    Converts a django auth User object to a FingrUser object
    """
    return FingrUser.objects.filter(django_user=django_user)[0]


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