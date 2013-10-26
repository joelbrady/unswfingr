import json
from django.db import models


class StaticLocation(models.Model):
    name = models.TextField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def _json(self):
        return json.dumps({'name': self.name, 'lat': self.latitude, 'lng': self.longitude, 'id': self.pk})

    json = property(_json)

    def __unicode__(self):
        return self.name + " lat: " + str(round(self.latitude, 4)) + " long: " + str(round(self.longitude, 4))
