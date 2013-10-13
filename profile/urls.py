from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^profile_course.html$', views.edit_course),
    url(r'^$', views.edit_profile),
)