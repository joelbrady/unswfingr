from django.forms import ModelForm
from django import forms
from profile.models import Profile
from profile.models import Course
from profile.models import Lecture, Tutorial, Labs
from profile.models import Day_Times
from profile.models import Custom_Times




class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('courses','custom_times')



class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('lectures', 'tutorials', 'labs')

class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ('day_time',)

class TutorialForm(ModelForm):
    class Meta:
        model = Tutorial
        exclude = ('day_time',)

class LabForm(ModelForm):
    class Meta:
        model = Labs
        exclude = ('day_time',)

class DayTimesForm(ModelForm):
    class Meta:
        model = Day_Times

class CustomTimesForm(ModelForm):
    class Meta:
        model = Custom_Times

class UploadFileForm(forms.Form):
    file  = forms.FileField()