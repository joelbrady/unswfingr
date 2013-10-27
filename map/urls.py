from django.conf.urls import patterns, url
from map import views

urlpatterns = patterns('',
    url(r'^$', views.view_map),
    url(r'^new_static$', views.new_static_marker),
    url(r'^update_static$', views.update_static_marker),
    url(r'^get_static$', views.get_static_markers),
    url(r'^set_my_marker$', views.set_my_marker),
    url(r'^get_my_marker$', views.get_my_marker)
)