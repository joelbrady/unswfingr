from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^profile_course.html$', views.edit_course),
    url(r'^edit_profile$', views.edit_profile),
)