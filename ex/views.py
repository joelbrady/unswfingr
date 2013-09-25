from django.http import HttpResponse
from django.template.loader import get_template


def index(request):
    return HttpResponse('Hello, world. Russ was here');

def testPage(request):
    t = get_template('test.html')
    headerText='our header will go in here'
    html = t.render(Context({'header': headerText}))
    return HttpResponse(html)

