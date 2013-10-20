from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',

    url(r'^$',views.index),
    url(r'^edit_courses', views.edit_course),
    url(r'^done_adding_courses', views.done),
    #url(r'^profile_course.html$', views.edit_course),
    url(r'^edit_profile$', views.edit_profile),

)