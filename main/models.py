from django.db import models


class Message(models.Model):
    text = models.EmailField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    sentFrom = models.ForeignKey('registration.FingrUser')

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