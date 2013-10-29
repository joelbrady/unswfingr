from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'(\d+)/?$',views.view_profile),
    url(r'^automatic_is_available', views.automatic_is_available),
    url(r'^edit_courses', views.edit_course),
    url(r'^edit_profile', views.edit_profile),
)
