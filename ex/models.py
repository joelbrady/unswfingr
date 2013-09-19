from django.db import models

class Person(models.Model):
    # a person just has a name
    name = models.CharField(max_length=100)

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return self.name
