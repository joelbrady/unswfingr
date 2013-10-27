import json
from django.db import models


class StaticLocation(models.Model):
    name = models.TextField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.name + " lat: " + str(round(self.latitude, 4)) + " long: " + str(round(self.longitude, 4))


class UserLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return "lat: " + str(round(self.latitude, 4)) + " long: " + str(round(self.longitude, 4))