from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_friend/(\d+)/?$', views.add_friend),
    url(r'^status$', views.set_status),
    url(r'^friends$', views.friends),
    url(r'^message/?$', views.inbox),
    url(r'^message/(\d+)/?$', views.message),
    url(r'^inbox/?$', views.inbox),
    url(r'^search$', views.search),
    url(r'^activate', views.activate),
    url(r'^set_online$', views.set_online),
    url(r'^set_offline', views.set_offline),
<<<<<<< HEAD
    url(r'^set_automatic', views.set_automatic),
=======
    url(r'^events?', views.events),
    url(r'^delete_event/(\d+)/?$', views.delete_event),
>>>>>>> 169fac3aeac10cdb0fc3d697928b1dc3fbf13e01

)