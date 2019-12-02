from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.utils import lorem_ipsum


urlpatterns = [
    path('', lambda request: HttpResponseRedirect(reverse('hello').rstrip('/'))),
    path('hello/', lambda request: HttpResponseRedirect(reverse('hello', kwargs={'name': 'world'}).rstrip('/')), name='hello'),
    path('hello/<name>/', lambda request, name: HttpResponse(
        f'<!doctype html>'
        f'<title>Hello {name}</title>'
        f'<h1>Hello {name}</h1>'
        f'{"<p>".join(lorem_ipsum.paragraphs(1))}'
    ), name='hello'),
]
