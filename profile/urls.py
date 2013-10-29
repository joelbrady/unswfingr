from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'(\d+)/?$',views.view_profile),
    url(r'^automatic_is_available', views.automatic_is_available),
    url(r'^edit_courses', views.edit_course),
    url(r'^edit_profile', views.edit_profile),
    url(r'add_custom_times', views.add_custom_times),
    url(r'add_courses_automatically', views.add_courses_automatically),

)
