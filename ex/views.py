from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template


def index(request):
    return HttpResponse('Hello, world. Russ was here');

def testPage(request):
    return render(request, 'test.html');

