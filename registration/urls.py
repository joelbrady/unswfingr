from django.conf.urls import patterns, url
from registration import views

urlpatterns = patterns('',
    url(r'^$', views.register),
)