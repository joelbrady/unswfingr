from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, RequestContext, loader
from django.template.loader import get_template



def index(request):
    return HttpResponse('Hello, world. Russ was here');

def testPage(request):

    template = loader.get_template('test.html')
    context = RequestContext(request, {
        'logged_in': False,
    })
    return HttpResponse(template.render(context))
