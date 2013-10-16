from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin interface
    url(r'^admin/', include(admin.site.urls)),

    # new user registration
    url(r'^registration/', include('registration.urls')),

    #profile page
    url(r'^profile/', include('profile.urls')),

    # main index page
    url(r'^', include('main.urls')),
)
