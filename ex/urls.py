from django.conf.urls import patterns, url
from ex import views

urlpatterns = patterns('',
    url(r'^index.html$', views.index, name='index'),
    url(r'^test.html*$', views.testPage),
)
