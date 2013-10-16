from django.db import models

class Message(models.Model):
    text = models.EmailField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    sentFrom = models.EmailField(max_length=100)


