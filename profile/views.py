# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from profile.forms import ProfileForm, CourseForm, LectureForm, DayTimesForm, TutorialForm, LabForm
#from profile.forms import CourseForm
from profile.models import Profile, Course, Lecture, Tutorial, Labs, Day_Times
from django.http import HttpResponse
from django.forms.formsets import formset_factory, BaseFormSet
from django.template import RequestContext
from registration.models import user_to_fingr
from registration.forms import FingrUserForm

def view_profile(request):

    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)

        c = {'username': f_user.username,
             'email': f_user.email,
             'first_name':f_user.first_name,
             'last_name': f_user.last_name,
            }
        return render_to_response('profile.html', c, context_instance = RequestContext(request))
    else:

        return render_to_response('need_to_login.html')


def edit_profile(request):



    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)


        profile_form = FingrUserForm(initial= {'username':f_user.username , 'email': f_user.email, 'first_name': f_user.first_name ,
                                             'last_name': f_user.last_name})

        if request.method == "POST":

            profile_form = FingrUserForm( request.POST, request.FILES)
            if profile_form.is_valid():
                f_user.username = profile_form.cleaned_data['username']
                f_user.email = profile_form.cleaned_data['email']
                f_user.first_name = profile_form.cleaned_data['first_name']
                f_user.last_name = profile_form.cleaned_data['last_name']
                f_user.save()


                return  render_to_response('updated_profile.html')
            else:
                print profile_form.errors

        return render_to_response('edit_profile.html', {'profile_form': profile_form, }, context_instance = RequestContext(request))
    else:

        return render_to_response('need_to_login.html')


def edit_course(request):
    #This class is used to make empty formset forms required
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

    if request.user.is_authenticated():
        user = user_to_fingr(request.user)


        profile = Profile.objects.get(fingr_user=user)


        if request.method == 'POST': # If the form has been submitted...

            course_formset = CourseFormSet(request.POST, prefix='course' )
            lecture_formset = LectureFormSet(request.POST, prefix='lecture')
            #lec_day_time_formset = DayTimeFormSet(request.POST,prefix='lec_day_time')
            tutorial_formset = TutorialFormSet(request.POST, prefix='tutorial')
            #tut_day_time_formset = DayTimeFormSet(request.POST, prefix='tut_day_time')
            laboratory_formset = LaboratoryFormSet(request.POST, prefix='laboratory')
            #lab_day_time_formset = DayTimeFormSet(request.POST, prefix='lab_day_time')


            if course_formset.is_valid() and lecture_formset.is_valid() and tutorial_formset.is_valid() and laboratory_formset.is_valid():
                #course_formset.save()
                #lecture_formset.save()
                #lec_day_time_formset.save()
                #tutorial_formset.save()
                #tut_day_time_formset.save()
                #laboratory_formset.save()

                print "ITS VALIDDASFJASFHSAHFQA"
                #print course_formset.getitem(0)
                for form in course_formset:
                    course = Course(course_name = form.cleaned_data['course_name'] , course_code = form.cleaned_data['course_code'])
                    course.save()




                for lec_form in lecture_formset:
                    lecture = Lecture(lecture_name = lec_form.cleaned_data['lecture_name'], choices_of_days = lec_form.cleaned_data['choices_of_days'],
                                      start_time = lec_form.cleaned_data['start_time'], end_time = lec_form.cleaned_data['end_time'])
                    lecture.save()
                    course.lectures.add(lecture)

                for tut_form in tutorial_formset:
                   tut = Tutorial(tutorial_name = tut_form.cleaned_data['tutorial_name'], choices_of_days = tut_form.cleaned_data['choices_of_days'],
                                  start_time = tut_form.cleaned_data['start_time'], end_time = tut_form.cleaned_data['end_time'])
                   tut.save()
                   course.tutorials.add(tut)

                for lab_form in laboratory_formset:
                   lab = Labs(lab_name = lab_form.cleaned_data['lab_name'], choices_of_days = lab_form.cleaned_data['choices_of_days'],
                                  start_time = lab_form.cleaned_data['start_time'], end_time = lab_form.cleaned_data['end_time'])
                   lab.save()
                   course.labs.add(lab)


                profile.courses.add(course)

                profile.save()



                for course in profile.courses.all():
                    print course.course_code
                    print course.course_name

                    for lecture in course.lectures.all():
                        print lecture.lecture_name
                        print lecture.start_time
                        print lecture.end_time
                        print lecture.choices_of_days




            else :
                course_formset.errors
                lecture_formset.errors
                #lec_day_time_formset.errors
                tutorial_formset.errors
                #tut_day_time_formset.errors
                laboratory_formset.errors
                #lab_day_time_formset.errors

            # Not in the else.
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
    else:

        return render_to_response('need_to_login.html')






