import datetime
from django import forms
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH
from django.forms import ModelForm
from django.forms.extras import SelectDateWidget
from django.utils import timezone
from main.models import Event


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'autofocus':'true'}))
    password = forms.CharField(widget=forms.PasswordInput(), max_length=MAXIMUM_PASSWORD_LENGTH)


class StatusForm(forms.Form):
    STATUS_CHOICES = (('ON', 'Available'),
                      ('OFF', 'Not Free'))
    available = forms.ChoiceField(choices=STATUS_CHOICES)

    #amount = forms.IntegerField(min_value=5, max_value=120)


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'true'}), max_length=MAXIMUM_PASSWORD_LENGTH)

class ActivateForm(forms.Form):
    activate = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=MAXIMUM_PASSWORD_LENGTH)


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = "Day"
        self.fields['timeStart'].label = 'Start time: (24 hour time HH:MM)'
        self.fields['timeEnd'].label = 'End time: (24 hour time HH:MM)'

        self.fields['timeStart'].input_formats= ('%H:%M',)
        self.fields['timeEnd'].input_formats= ('%H:%M',)
    class Meta:
        model = Event
        fields=['title','date','timeStart','timeEnd','description']


        thisYear = datetime.date.today().year

        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'E.g Party at CSE'}),
            'date': SelectDateWidget(years=range(thisYear, thisYear+2)),
            'timeStart': forms.TextInput(attrs={'placeholder':'E.g. 7:00, 14:30'}),
            'timeEnd': forms.TextInput(attrs={'placeholder':'E.g. 9:00, 17:00'}),
            'description': forms.Textarea(),


        }






