from django.db import models

days = (

     ('MON', 'Monday'),
     ('TUE', 'Tuesday'),
     ('WED', 'Wednesday'),
     ('THU', 'Thursday'),
     ('FRI', 'Friday'),

)

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

### Create your models here.
class Day_Times(models.Model):


    choices_of_days = models.CharField(max_length=3,
                                      choices=days,
                                      default='MON')


    start_time = models.CharField(max_length=2,
                                      choices=times,
                                      default='9')

    end_time = models.CharField(max_length=2,
                                      choices=times,
                                      default='10')




class Profile(models.Model):
    ## a profile has the person
    #username = models.CharField(max_length=100)
    #
    #email = models.EmailField(max_length=100)#models.ForeignKey(Person, to_field=name) # We prefer person.name as this will get our email from person class. FIX LATER!
    #phone = models.IntegerField()
    courses = models.ManyToManyField('Course')
    custom_times = models.ManyToManyField('Custom_Times')

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return self.fingr_user.username


class Lecture(models.Model):
    choice_of_day = models.CharField(max_length=3,choices=days)
    start_time = models.CharField(max_length=2,choices=times)
    end_time = models.CharField(max_length=2,choices=times)

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Lecture model'

class Tutorial(models.Model):
    choice_of_day = models.CharField(max_length=3,choices=days)
    start_time = models.CharField(max_length=2,choices=times)
    end_time = models.CharField(max_length=2,choices=times)


    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Tutorial model'

class Labs(models.Model):
    choice_of_day = models.CharField(max_length=3,choices=days)
    start_time = models.CharField(max_length=2,choices=times)
    end_time = models.CharField(max_length=2,choices=times)

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Lab model'

class Custom_Times(models.Model):
    name = models.CharField(max_length=100)
    choice_of_day = models.CharField(max_length=3,choices=days)
    start_time = models.CharField(max_length=2,choices=times)
    end_time = models.CharField(max_length=2,choices=times)

    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return 'Custom Times Model'

class Course(models.Model):
    course_code = models.CharField(max_length=8)
    course_name = models.CharField(max_length=100)
    lectures = models.ManyToManyField(Lecture, related_name='lecture_times')
    tutorials = models.ManyToManyField(Tutorial, related_name='tutorials_times')
    labs = models.ManyToManyField(Labs, related_name='lab_times')


    def __unicode__(self):
        # this method is used when an instance of this
        # is printed in the interactive shell
        return self.name







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