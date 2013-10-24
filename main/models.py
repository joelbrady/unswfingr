import json
from django.db import models


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


class StaticLocation(models.Model):
    name = models.TextField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def _json(self):
        return json.dumps({'name': self.name, 'lat': self.latitude, 'lng': self.longitude, 'id': self.pk})

    json = property(_json)

    def __unicode__(self):
        return self.name + " lat: " + str(round(self.latitude, 4)) + " long: " + str(round(self.longitude, 4))
