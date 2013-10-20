# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from profile.forms import ProfileForm, CourseForm, LectureForm, DayTimesForm, TutorialForm, LabForm
#from profile.forms import CourseForm
from profile.models import Profile, Course
from django.http import HttpResponse
from django.forms.formsets import formset_factory, BaseFormSet
from django.template import RequestContext


#testing stuff
def index(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False



    CourseFormSet = formset_factory(CourseForm, max_num=10, formset=RequiredFormSet)
    LectureFormSet = formset_factory(LectureForm, max_num=10, formset=RequiredFormSet)
    TutorialFormSet = formset_factory(TutorialForm, max_num=10, formset=RequiredFormSet)
    LaboratoryFormSet = formset_factory(LabForm, max_num=10, formset=RequiredFormSet)
    DayTimeFormSet = formset_factory(DayTimesForm,max_num=10, formset=RequiredFormSet)

    if request.method == 'POST': # If the form has been submitted...
        profile_form = ProfileForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        course_formset = CourseFormSet(request.POST, request.FILES, prefix='course')
        lecture_formset = LectureFormSet(request.POST, request.FILES, prefix='lecture')

        if profile_form.is_valid() and course_formset.is_valid() and lecture_formset.is_valid():
            #courses = profile_form.save()
            for form in course_formset.forms:
                print form.cleaned_data['course_name']

            for lec_form in lecture_formset.forms:
                 print lec_form.cleaned_data['lecture_name']
                 print "test"

                #todo_item = form.save(commit=False)
                #todo_item.list = courses
                #todo_item.save()
            return HttpResponse(profile_form.cleaned_data['email']) # Redirect to a 'success' page
        else :
            return HttpResponse('test')
    else:
        profile_form = ProfileForm()
        course_formset = CourseFormSet(prefix='course')
        lecture_formset = LectureFormSet(prefix='lecture')
        day_time_formset = DayTimeFormSet(prefix='day_time')
        tutorial_formset = TutorialFormSet(prefix='tutorial')
        laboratory_formset = LaboratoryFormSet(prefix='laboratory')

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    c = {'profile_form': profile_form,
         'course_formset': course_formset,
         'lecture_formset': lecture_formset,
         'day_time_formset': day_time_formset,
         'tutorial_formset': tutorial_formset,
         'laboratory_formset': laboratory_formset,
        }
    #c.update(csrf(request))

    return render_to_response('profile.html', c,  context_instance=RequestContext(request))


#
#def edit_profile(request):
#    if request.method == "POST":
#
#        profile_form = ProfileForm( request.POST, request.FILES)
#        course_form = CourseForm(request.POST, request.FILES)
#        lecture_form = LectureForm(request.POST, request.FILES)
#        day_times_form = DayTimesForm(request.POST, request.FILES)
#        tutorial_form = TutorialForm(request.POST, request.FILES)
#        lab_form = LabForm(request.POST, request.FILES)
#
#        if profile_form.is_valid() and course_form.is_valid() and lecture_form.is_valid() and day_times_form.is_valid() and tutorial_form.is_valid() and lab_form.is_valid():
#            profile_form.save()
#            course_form.save()
#            lecture_form.save()
#            day_times_form.save()
#            tutorial_form.save()
#            lab_form.save()
#            # Do something. Should generally end with a redirect. For example:
#            return  HttpResponse('Your profile has been updated')
#        else:
#            print profile_form.errors
#            print course_form.errors
#            print lecture_form.errors
#            print day_times_form.errors
#            print tutorial_form.errors
#            print lab_form.errors
#
#    else:
#        profile_form = ProfileForm()
#        course_form = CourseForm()
#        lecture_form = LectureForm()
#        day_times_form = DayTimesForm()
#        tutorial_form = TutorialForm()
#        lab_form = LabForm()
#
#    return render_to_response('profile.html', {
#    'profile_form': profile_form,
#    'course_form': course_form,
#    'lecture_form': lecture_form,
#    'day_times_form': day_times_form,
#    'tutorial_form' : tutorial_form,
#    'lab_form' : lab_form}, context_instance = RequestContext(request))

def edit_course(request):
    return render_to_response('profile_course.html', context_instance = RequestContext(request))

