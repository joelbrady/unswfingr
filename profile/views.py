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


    if request.method == 'POST': # If the form has been submitted...
        profile_form = ProfileForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data


        if profile_form.is_valid() :
            #courses = profile_form.save()

                #todo_item = form.save(commit=False)
                #todo_item.list = courses
                #todo_item.save()
            return HttpResponse(profile_form.cleaned_data['email']) # Redirect to a 'success' page
        else :
            return HttpResponse('test')
    else:
        profile_form = ProfileForm()


    # For CSRF protection

    #c.update(csrf(request))

    return render_to_response('edit_profile.html', {'profile_form': profile_form},  context_instance=RequestContext(request))


def edit_course(request):
    #This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False


    print request

    CourseFormSet = formset_factory(CourseForm, max_num=10, formset=RequiredFormSet)
    LectureFormSet = formset_factory(LectureForm, max_num=10, formset=RequiredFormSet)
    TutorialFormSet = formset_factory(TutorialForm, max_num=10, formset=RequiredFormSet)
    LaboratoryFormSet = formset_factory(LabForm, max_num=10, formset=RequiredFormSet)
    DayTimeFormSet = formset_factory(DayTimesForm,max_num=10, formset=RequiredFormSet)

    if request.method == 'POST': # If the form has been submitted...
        course_formset = CourseFormSet(request.POST, prefix='course' )
        lecture_formset = LectureFormSet(request.POST, prefix='lecture')
        day_time_formset = DayTimeFormSet(request.POST, prefix='day_time')
        tutorial_formset = TutorialFormSet(request.POST, prefix='tutorial')
        laboratory_formset = LaboratoryFormSet(request.POST, prefix='laboratory')
        for form in course_formset:
            print form

        if course_formset.is_valid() and lecture_formset.is_valid() and day_time_formset.is_valid() and tutorial_formset.is_valid() and laboratory_formset.is_valid():
            course_formset.save()
            lecture_formset.save()
            day_time_formset.save()
            tutorial_formset.save()
            laboratory_formset.save()
        else :
            course_formset.errors
            lecture_formset.errors
            day_time_formset.errors
            tutorial_formset.errors
            laboratory_formset.errors

        return render_to_response('add_courses.html')

    course_formset = CourseFormSet(prefix='course')
    lecture_formset = LectureFormSet(prefix='lecture')
    day_time_formset = DayTimeFormSet(prefix='day_time')
    tutorial_formset = TutorialFormSet(prefix='tutorial')
    laboratory_formset = LaboratoryFormSet(prefix='laboratory')

    c = {'course_formset': course_formset,
         'lecture_formset': lecture_formset,
         'day_time_formset': day_time_formset,
         'tutorial_formset': tutorial_formset,
         'laboratory_formset': laboratory_formset,
        }

    return render_to_response('edit_courses.html',c, context_instance = RequestContext(request))




def edit_profile(request):
    if request.method == "POST":
        profile_form = ProfileForm( request.POST, request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            return  HttpResponse('Your profile has been updated')
        else:
            print profile_form.errors

    else:
        profile_form = ProfileForm()


    return render_to_response('edit_profile.html', {'profile_form': profile_form, }, context_instance = RequestContext(request))



