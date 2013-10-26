from django.contrib import admin
from map.models import StaticLocation, UserLocation


admin.site.register(StaticLocation)
admin.site.register(UserLocation)