# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from profile.forms import ProfileForm, CourseForm, LectureForm, DayTimesForm, TutorialForm, LabForm
#from profile.forms import CourseForm
from profile.models import Profile, Course
from django.http import HttpResponse
from django.template import RequestContext



def edit_profile(request):
    if request.method == "POST":

        profile_form = ProfileForm( request.POST, request.FILES)
        course_form = CourseForm(request.POST, request.FILES)
        lecture_form = LectureForm(request.POST, request.FILES)
        day_times_form = DayTimesForm(request.POST, request.FILES)
        tutorial_form = TutorialForm(request.POST, request.FILES)
        lab_form = LabForm(request.POST, request.FILES)

        if profile_form.is_valid() and course_form.is_valid() and lecture_form.is_valid() and day_times_form.is_valid() and tutorial_form.is_valid() and lab_form.is_valid():
            profile_form.save()
            course_form.save()
            lecture_form.save()
            day_times_form.save()
            tutorial_form.save()
            lab_form.save()
            # Do something. Should generally end with a redirect. For example:
            return  HttpResponse('Your profile has been updated')
        else:
            print profile_form.errors
            print course_form.errors
            print lecture_form.errors
            print day_times_form.errors
            print tutorial_form.errors
            print lab_form.errors

    else:
        profile_form = ProfileForm()
        course_form = CourseForm()
        lecture_form = LectureForm()
        day_times_form = DayTimesForm()
        tutorial_form = TutorialForm()
        lab_form = LabForm()

    return render_to_response('profile.html', {
    'profile_form': profile_form,
    'course_form': course_form,
    'lecture_form': lecture_form,
    'day_times_form': day_times_form,
    'tutorial_form' : tutorial_form,
    'lab_form' : lab_form}, context_instance = RequestContext(request))