from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_friend/([^/]+)/?$', views.add_friend),
    url(r'^status$', views.set_status),
    url(r'^friends$', views.friends),
<<<<<<< HEAD
    url(r'^search$', views.search),
    url(r'^activate$', views.activate),
=======
    url(r'^message/(\d+)/?$', views.message),
    url(r'^map$', views.view_map),
    url(r'^inbox/?$', views.inbox),


>>>>>>> dd1ea724a30bc9ee0c6280ba9d3c26e11afab538
)