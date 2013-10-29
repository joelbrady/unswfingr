# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from ihooks import current_importer
from profile.forms import ProfileForm, CourseForm, LectureForm, DayTimesForm, TutorialForm, LabForm
#from profile.forms import CourseForm
from profile.models import Profile, Course, Lecture, Tutorial, Labs, Day_Times
from django.http import HttpResponse
from django.forms.formsets import formset_factory, BaseFormSet
from django.template import RequestContext
from registration.models import user_to_fingr
from registration.models import FingrUser
from registration.forms import FingrUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import itertools
import datetime
from django.shortcuts import render, redirect


#remove foreign  key, change around so that ufingr has profile field

#availability, Property ( Fingr user fo r friends list)
#add drop down
# scrub the input data for courses. OPTIONAL
# start time and end time for courses


# Determines if a user is unavailable based of their timetable data.
def automatic_is_available(request):
    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)
        f_user.automatic_availability = True
        current_hour =  datetime.datetime.now().hour
        current_day = datetime.datetime.now().strftime("%A")

        f_user.available = True

        for course in f_user.profile.courses.all():
            for lecture in course.lectures.all():
                if(int(lecture.start_time) <= current_hour):
                    if(int(lecture.end_time) > current_hour ):
                        if(str(lecture.choice_of_day).lower() in current_day.lower()):
                            f_user.available = False
            for tutorial in course.tutorials.all() :
                if(int(tutorial.start_time) <= current_hour):
                    if(int(tutorial.end_time) > current_hour ):
                        if(str(lecture.choice_of_day).lower() in current_day.lower()):
                            f_user.available = False
            for lab in course.labs.all() :
                if(int(lab.start_time) <= current_hour):
                    if(int(lab.end_time) > current_hour ):
                       if(str(lecture.choice_of_day).lower() in current_day.lower()):
                            f_user.available = False
        f_user.save()

    #return redirect('main.views.index')



@login_required
def view_profile(request, target_user_pk):
    print "target user" + target_user_pk

    if request.user.is_authenticated():
        #f_user = FingrUser.objects.filter(pk=target_user_pk)[0]
        f_user = get_object_or_404( FingrUser.objects,pk=target_user_pk)

        profile = f_user.profile

        # Trying to print courses in a graphical way.
        #for course in profile.courses.all():
        #    print course.course_code
        #    print course.course_name
        #
        #
        #ordered_courses = { }
        monday = ""
        tuesday = ""
        wednesday = ""
        thursday = ""
        friday = ""
        for course in profile.courses.all():
            for lecture in course.lectures.all():
                if lecture.choice_of_day == "MON":
                    monday = monday + course.course_code + "\t" +"Lecture" + "\t" + lecture.start_time + "-" + lecture.end_time + "\n"
                elif lecture.choice_of_day == "TUE":
                    tuesday = tuesday + course.course_code + "\t" +"Lecture" + "\t" + lecture.start_time + "-" + lecture.end_time + "\n"
                elif lecture.choice_of_day == "WED":
                    wednesday = wednesday + course.course_code + "\t" +"Lecture" + "\t" + lecture.start_time + "-" + lecture.end_time + "\n"
                elif lecture.choice_of_day == "THU":
                    thursday = thursday + course.course_code + "\t" +"Lecture" + "\t" + lecture.start_time + "-" + lecture.end_time + "\n"
                elif lecture.choice_of_day == "FRI":
                    friday = friday + course.course_code + "\t" +"Lecture" + "\t" + lecture.start_time + "-" + lecture.end_time + "\n"

            for tutorial in course.tutorials.all() :
                if tutorial.choice_of_day == "MON":
                    monday = monday + course.course_code + "\t" + "Tutorial" + "\t" + tutorial.start_time + "-" + tutorial.end_time + "\n"
                elif tutorial.choice_of_day == "TUE":
                    tuesday = tuesday + course.course_code + "\t" + "Tutorial" + "\t" + tutorial.start_time + "-" + tutorial.end_time + "\n"
                elif tutorial.choice_of_day == "WED":
                    wednesday = wednesday + course.course_code + "\t" + "Tutorial" + "\t" + tutorial.start_time + "-" + tutorial.end_time + "\n"
                elif tutorial.choice_of_day == "THU":
                    thursday = thursday + course.course_code + "\t" + "Tutorial" + "\t" + tutorial.start_time + "-" + tutorial.end_time + "\n"
                elif tutorial.choice_of_day == "FRI":
                    friday = friday + course.course_code + "\t" + "Tutorial" + "\t" + tutorial.start_time + "-" + tutorial.end_time + "\n"

            for lab in course.labs.all() :
                if lab.choice_of_day == "MON":
                    monday = monday + course.course_code + "\t" + "Lab" + "\t" + lab.start_time + "-"  + lab.end_time + "\n"
                elif lab.choice_of_day == "TUE":
                    tuesday = tuesday + course.course_code + "\t" + "Lab" + "\t" + lab.start_time + "-" + lab.end_time + "\n"
                elif lab.choice_of_day == "WED":
                    wednesday = wednesday + course.course_code + "\t" + "Lab" + "\t" + lab.start_time + "-" + lab.end_time + "\n"
                elif lab.choice_of_day == "THU":
                    thursday = thursday + course.course_code + "\t" + "Lab" + "\t" + lab.start_time + "-" + lab.end_time + "\n"
                elif lab.choice_of_day == "FRI":
                    friday = friday + course.course_code + "\t" + "Lab" + "\t" + lab.start_time + "-" + lab.end_time + "\n"

        monday = monday.strip("\n")
        tuesday = tuesday.strip("\n")
        wednesday = wednesday.strip("\n")
        thursday = thursday.strip("\n")
        friday = friday.strip("\n")

        monday_dict = monday.split("\n")
        tuesday_dict = tuesday.split("\n")
        wednesday_dict = wednesday.split("\n")
        thursday_dict = thursday.split("\n")
        friday_dict = friday.split("\n")

        final_monday = []
        final_tuesday = []
        final_wednesday = []
        final_thursday = []
        final_friday = []
        for sub in monday_dict:
            for splitted in sub.split("\t"):
                final_monday.append(splitted)

        for sub in tuesday_dict:
            for splitted in sub.split("\t"):
                final_tuesday.append(splitted)

        for sub in wednesday_dict:
            for splitted in sub.split("\t"):
                final_wednesday.append(splitted)

        for sub in thursday_dict:
            for splitted in sub.split("\t"):
                final_thursday.append(splitted)

        for sub in friday_dict:
            for splitted in sub.split("\t"):
                final_friday.append(splitted)


        iterator =  itertools.count()
        iterator2 = itertools.count()
        iterator3 = itertools.count()
        iterator4 = itertools.count()
        iterator5 = itertools.count()

        me_f_user = user_to_fingr(request.user)

        target_user_pk = int(target_user_pk)
        is_friend = False
        for friend in me_f_user.friends_list:
            if friend.pk == target_user_pk:
                is_friend = True



        c = {'username': f_user.username,
            'email': f_user.email,
            'first_name':f_user.first_name,
            'last_name': f_user.last_name,
            'monday': final_monday,
            'tuesday': final_tuesday,
            'wednesday': final_wednesday,
            'thursday': final_thursday,
            'friday': final_friday,
            'iterator': iterator,
            'iterator2': iterator2,
            'iterator3': iterator3,
            'iterator4': iterator4,
            'iterator5': iterator5,
            'target_user_pk': target_user_pk,
            'is_friend' : is_friend,

            }

        return render_to_response('profile.html', c, context_instance = RequestContext(request))
    else:

        return render_to_response('need_to_login.html')

@login_required
def edit_profile(request):



    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)


        profile_form = FingrUserForm(initial= {'first_name': f_user.first_name ,
                                             'last_name': f_user.last_name,
                                             'visibility': f_user.visibility},)

        if request.method == "POST":

            profile_form = FingrUserForm( request.POST, request.FILES)
            if profile_form.is_valid():

                f_user.first_name = profile_form.cleaned_data['first_name']
                f_user.last_name = profile_form.cleaned_data['last_name']
                f_user.visibility = profile.form.cleaned_data['visibility']
                f_user.save()


                return  render_to_response('updated_profile.html', context_instance = RequestContext(request))
            else:
                print profile_form.errors

        return render_to_response('edit_profile.html', {'profile_form': profile_form, }, context_instance = RequestContext(request))
    else:

        return render_to_response('need_to_login.html', context_instance = RequestContext(request))

@login_required
def edit_course(request):
    #This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False




    CourseFormSet = formset_factory(CourseForm, max_num=10, formset=RequiredFormSet)
    LectureFormSet = formset_factory(LectureForm, extra = 1, max_num=10, formset=RequiredFormSet)
    TutorialFormSet = formset_factory(TutorialForm, max_num=10, formset=RequiredFormSet)
    LaboratoryFormSet = formset_factory(LabForm, max_num=10, formset=RequiredFormSet)
    DayTimeFormSet = formset_factory(DayTimesForm,max_num=10, formset=RequiredFormSet)

    if request.user.is_authenticated():
        f_user = user_to_fingr(request.user)


        #profile = f_user.profile.objects.get(fingr_user=f_user)
        profile = f_user.profile


        if request.method == 'POST': # If the form has been submitted...

            course_formset = CourseFormSet(request.POST, prefix='course' )
            lecture_formset = LectureFormSet(request.POST, prefix='lecture')
            #lec_day_time_formset = DayTimeFormSet(request.POST,prefix='lec_day_time')
            tutorial_formset = TutorialFormSet(request.POST, prefix='tutorial')
            #tut_day_time_formset = DayTimeFormSet(request.POST, prefix='tut_day_time')
            laboratory_formset = LaboratoryFormSet(request.POST, prefix='laboratory')
            #lab_day_time_formset = DayTimeFormSet(request.POST, prefix='lab_day_time')


            if course_formset.is_valid():
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

                if lecture_formset.is_valid():
                    for lec_form in lecture_formset:
                        # need to figure out a way to compare theses and print an error !!!
                        print lec_form.cleaned_data['start_time']
                        print lec_form.cleaned_data['end_time']
                        lecture = Lecture(choice_of_day = lec_form.cleaned_data['choice_of_day'],
                                          start_time = lec_form.cleaned_data['start_time'], end_time = lec_form.cleaned_data['end_time'])
                        lecture.save()
                        course.lectures.add(lecture)

                if tutorial_formset.is_valid():
                    for tut_form in tutorial_formset:
                       tut = Tutorial(choice_of_day = tut_form.cleaned_data['choice_of_day'],
                                      start_time = tut_form.cleaned_data['start_time'], end_time = tut_form.cleaned_data['end_time'])
                       tut.save()
                       course.tutorials.add(tut)

                if laboratory_formset.is_valid():
                    for lab_form in laboratory_formset:
                       lab = Labs( choice_of_day = lab_form.cleaned_data['choice_of_day'],
                                      start_time = lab_form.cleaned_data['start_time'], end_time = lab_form.cleaned_data['end_time'])
                       lab.save()
                       course.labs.add(lab)


                profile.courses.add(course)

                profile.save()
                # Not in the else.
                return render_to_response('add_courses.html', context_instance = RequestContext(request))

            else :
                print course_formset.errors
                print lecture_formset.errors
                #lec_day_time_formset.errors
                print tutorial_formset.errors
                #tut_day_time_formset.errors
                print laboratory_formset.errors
                #lab_day_time_formset.errors



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

        return render_to_response('need_to_login.html', context_instance = RequestContext(request))






