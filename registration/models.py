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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def get_username(self):
        return self.django_user.username

def create_fingr_user(email, password, **kwargs):
    """
    This function takes clean data to create a fingr user,
    please do not create one yourself
    """
    django_user = User.objects.create_user(username=email, email=email, password=password)
    fingr_user = FingrUser(django_user=django_user, **kwargs)
    fingr_user.save()
    return fingr_user