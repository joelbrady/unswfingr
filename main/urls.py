from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_friend/([^/]+)/?$', views.add_friend),
    url(r'^status$', views.set_status),
    url(r'^friends$', views.friends),
)