from django.contrib.auth.models import User
from django.db import models
from main.globals import UNSW_LATITUDE, UNSW_LONGITUDE
from main.models import Message
from map.models import StaticLocation
from profile.models import Profile
from map.models import UserLocation


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
    static_locations = models.ManyToManyField(StaticLocation)
    profile = models.ForeignKey(Profile, unique=True)
    my_location = models.ForeignKey(UserLocation)
    visibility_hide = 'None'
    visibility_friends = 'Friends'
    visibility_all = 'All'
    visibility_choices = (
        (visibility_hide, 'None'),
        (visibility_friends, 'Friends'),
        (visibility_all, 'All'),
    )
    visibility = models.CharField(max_length=7, choices=visibility_choices, default=visibility_all)

    def _get_username(self):
        return self.django_user.username

    def _get_email(self):
        return self.django_user.email

    def _friends_list(self):
        return self.friends.all()

    def _messages_list(self):
        return self.messages.all()

    def _full_name(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        else:
            return self.username

    friends_list = property(_friends_list)

    messages_list = property(_messages_list)

    full_name = property(_full_name)

    def __unicode__(self):
        return self.username

    def verify(self):
        self.verified = True


def user_to_fingr(django_user):
    """
    Converts a django auth User object to a FingrUser object
    """
    return FingrUser.objects.get(django_user=django_user)


def create_fingr_user(email, password, **kwargs):
    """
    This function takes clean data to create a fingr user,
    please do not create one yourself
    """

    # the django create_user method automatically saves it in the database for us
    django_user = User.objects.create_user(username=email, email=email, password=password)

    initial_location = UserLocation(latitude=UNSW_LATITUDE, longitude=UNSW_LONGITUDE)
    initial_location.save()

    profile = Profile()
    profile.save()

    fingr_user = FingrUser(django_user=django_user, username=email, email=email, my_location=initial_location,
                           profile=profile, **kwargs)
    fingr_user.save()

    return fingr_user