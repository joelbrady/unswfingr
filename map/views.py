import json
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
import main
from main.models import Event
from map.models import StaticLocation
from registration.models import user_to_fingr


@login_required
def view_map(request):
    user = user_to_fingr(request.user)
    context = {'my_events': Event.objects.filter(owner=user),
               'friends_events': Event.objects.filter(owner__in=user.friends_list.all())}
    return render(request, 'map.html', context)


@login_required
def new_static_marker(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False}))

    name = request.POST.get('name', None)
    latitude = request.POST.get('lat', None)
    longitude = request.POST.get('lng', None)

    response = {'success': False}

    for x in (name, latitude, longitude):
        if x is None:
            return HttpResponse(json.dumps(response))
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return HttpResponse(json.dumps(response))

    loc = StaticLocation(name=name, latitude=latitude, longitude=longitude)
    loc.save()

    user = user_to_fingr(request.user)
    user.static_locations.add(loc)

    response['pk'] = loc.pk
    response['success'] = True

    return HttpResponse(json.dumps(response))


@login_required
def update_static_marker(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False}))

    pk = request.POST.get('id', None)
    latitude = request.POST.get('lat', None)
    longitude = request.POST.get('lng', None)

    for field in (pk, latitude, longitude):
        if field is None:
            return HttpResponse(json.dumps({'success': False}))

    try:
        pk = int(pk)
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return HttpResponse(json.dumps({'success': False}))

    static_marker_lookup = StaticLocation.objects.filter(pk=pk)
    assert len(static_marker_lookup) <= 1
    if len(static_marker_lookup) == 1:
        static_marker = static_marker_lookup[0]
        user = user_to_fingr(request.user)
        if user.static_locations.filter(pk=static_marker.pk).count() > 0:
            static_marker.latitude = latitude
            static_marker.longitude = longitude
            static_marker.save()
            return HttpResponse(json.dumps({'success': True}))
    return HttpResponse(json.dumps({'success': False}))


@login_required
def get_static_markers(request):
    user = user_to_fingr(request.user)
    assert user is not None

    response = []
    # get users' own markers
    for loc in user.static_locations.all():
        response.append(loc)
    # get all friends markers
    for friend in user.friends.all():
        for marker in friend.static_locations.all():
            response.append(marker)

    def model_to_dict_wrapper(instance):
        d = model_to_dict(instance, fields=['name', 'latitude', 'longitude'])
        d['id'] = instance.pk
        return d

    response = map(model_to_dict_wrapper, response)
    return HttpResponse(json.dumps(response))


@login_required
def set_my_marker(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False}))

    user = user_to_fingr(request.user)
    assert user is not None

    latitude = request.POST.get('lat', None)
    longitude = request.POST.get('lng', None)

    for field in (latitude, longitude):
        if field is None:
            return HttpResponse(json.dumps({'success': False}))

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return HttpResponse(json.dumps({'success': False}))

    my_location = user.my_location
    my_location.latitude = latitude
    my_location.longitude = longitude
    my_location.save()

    return HttpResponse(json.dumps({'success': True}))


@login_required
def get_my_marker(request):
    user = user_to_fingr(request.user)
    assert user is not None

    return HttpResponse(json.dumps(model_to_dict(user.my_location)))


@login_required
def get_friends_locations(request):
    user = user_to_fingr(request.user)
    assert user is not None

    response = []

    for friend in user.friends_list.all():
        loc = model_to_dict(friend.my_location)
        loc['name'] = friend.full_name
        response.append(loc)

    return HttpResponse(json.dumps(response))


@login_required
def get_events(request):
    user = user_to_fingr(request.user)
    assert user is not None

    response = []

    for event in Event.objects.filter(owner=user):
        e = model_to_dict(event, fields=['title', 'latitude', 'longitude'])
        e['owner'] = event.owner.full_name
        e['id'] = event.pk
        e['draggable'] = True
        response.append(e)

    for event in Event.objects.filter(owner__in=user.friends_list):
        e = model_to_dict(event, fields=['title', 'latitude', 'longitude'])
        e['owner'] = event.owner.full_name
        e['id'] = event.pk
        e['draggable'] = False
        response.append(e)

    return HttpResponse(json.dumps(response))


@login_required
def set_event_marker(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False}))

    user = user_to_fingr(request.user)
    assert user is not None

    latitude = request.POST.get('lat', None)
    longitude = request.POST.get('lng', None)
    pk = request.POST.get('id', None)

    for field in (latitude, longitude, pk):
        if field is None:
            return HttpResponse(json.dumps({'success': False}))

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        pk = int(pk)
    except ValueError:
        return HttpResponse(json.dumps({'success': False}))

    event = Event.objects.get(pk=pk)
    if event.owner != user:
        return HttpResponse(json.dumps({'success': False}))

    event.longitude = longitude
    event.latitude = latitude
    event.save()

    return HttpResponse(json.dumps({'success': True}))