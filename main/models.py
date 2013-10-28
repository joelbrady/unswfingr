import datetime
from django.db import models
from main.globals import UNSW_LATITUDE, UNSW_LONGITUDE


class Message(models.Model):
    text = models.EmailField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    sentFrom = models.ForeignKey('registration.FingrUser', related_name='sent_from_fingruser')
    sentTo = models.ForeignKey('registration.FingrUser', related_name='sent_to_fingruser')

    read = models.BooleanField(default=False)

    MESSAGE = 'M'
    NOTIFICATION = 'N'
    TYPE_CHOICES = ((NOTIFICATION, 'Notification'),
                    (MESSAGE, 'Message'),
                    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=NOTIFICATION)


class Event(models.Model):
    title = models.CharField(max_length=30)

    owner = models.ForeignKey('registration.FingrUser', related_name='event_owner')
    day = datetime.date.today
    date = models.DateField(default=day)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    description = models.CharField(max_length=5000)
    latitude = models.FloatField(default=UNSW_LATITUDE)
    longitude = models.FloatField(default=UNSW_LONGITUDE)

    def __unicode__(self):
        return self.title + " @ " + str(self.date)