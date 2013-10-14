from django.db import models
from ex.models import Person


### Create your models here.
class Day_Times(models.Model):
    days = (
         ('SUN', 'Sunday'),
         ('MON', 'Monday'),
         ('TUE', 'Tuesday'),
         ('WED', 'Wednesday'),
         ('THU', 'Thursday'),
         ('FRI', 'Friday'),
         ('SAT', 'Saturday'),
    )

    choices_of_days = models.CharField(max_length=3,
                                      choices=days,
                                      default='SUN')
    times = (
        ('8', '8 AM'),
        ('9', '9 AM'),
        ('10', '10 AM'),
        ('11', '11 AM'),
        ('12', '12 AM'),
        ('13', '1 PM'),
        ('14', '2 PM'),
        ('15', '3 PM'),
        ('16', '4 PM'),
        ('17', '5 PM'),
        ('18', '6 PM'),
        ('19', '7 PM'),
        ('20', '8 PM'),
        ('21', '9 PM'),
    )

    start_time = models.CharField(max_length=2,
                                      choices=times,
                                      default='9')

    end_time = models.CharField(max_length=2,
                                      choices=times,
                                      default='10')




class Profile(models.Model):
    # a profile has the person
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)#models.ForeignKey(Person, to_field=name) # We prefer person.name as this will get our email from person class. FIX LATER!
    phone = models.IntegerField()
    courses = models.ManyToManyField('Course')

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return self.name

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=8)
    lecture = models.ManyToManyField(Day_Times, related_name='lecture_times')
    tutorials = models.ManyToManyField(Day_Times, related_name='tutorials_times')
    labs = models.ManyToManyField(Day_Times, related_name='lab_times')


    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return self.name



class Lecture(models.Model):
    lecture_name = models.CharField(max_length=100)
    day_time = models.ManyToManyField(Day_Times)
    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Lecture model'

class Tutorial(models.Model):
    tutorial_name = models.CharField(max_length=100)
    day_time = models.ManyToManyField(Day_Times)
    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Tutorial model'

class Labs(models.Model):
    lab_name = models.CharField(max_length=100)
    day_time = models.ManyToManyField(Day_Times)
    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Lab model'




#
#class ProfileForm(ModelForm):
#    class Meta:
#        model = Profile
#x
#
#class CourseForm(ModelForm):
#    class Meta:
#        model = Course
#
#class DayTimeForm(ModelForm):
#    class Meta:
#        model = Day_Times