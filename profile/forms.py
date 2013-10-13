from django.forms import ModelForm
from profile.models import Profile
from profile.models import Course
from profile.models import Lecture, Tutorial, Labs
from profile.models import Day_Times




class ProfileForm(ModelForm):
    class Meta:
        model = Profile

class CourseForm(ModelForm):
    class Meta:
        model = Course

class LectureForm(ModelForm):
    class Meta:
        model = Lecture

class TutorialForm(ModelForm):
    class Meta:
        model = Tutorial;

class LabForm(ModelForm):
    class Meta:
        model = Labs

class DayTimesForm(ModelForm):
    class Meta:
        model = Day_Times

