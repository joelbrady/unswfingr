from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_friend/(\d+)/?$', views.add_friend),
    url(r'^status$', views.set_status),
    url(r'^friends$', views.friends),
    url(r'^message/(\d+)/?$', views.message),
    url(r'^map$', views.view_map),
    url(r'^inbox/?$', views.inbox),
    url(r'^search$', views.search),
    url(r'^activate', views.activate),
)