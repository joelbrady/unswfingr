from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^$', views.edit_profile),
)