from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',

    url(r'/(\d+)/?$',views.view_profile),

    url(r'^edit_courses', views.edit_course),

    #url(r'^add_courses.html$', views.edit_course),
    url(r'^edit_profile', views.edit_profile),

)