from django.http import HttpResponse
from django.urls import path, reverse
from django.utils import lorem_ipsum

from .http import Http2ServerPushPermanentRedirect


urlpatterns = [
    path('', lambda request: Http2ServerPushPermanentRedirect(reverse('hello'))),
    path('hello/', lambda request: Http2ServerPushPermanentRedirect(reverse('hello', kwargs={'name': 'world'})), name='hello'),
    path('hello/<name>/', lambda request, name: HttpResponse(
        f'<!doctype html>'
        f'<title>Hello {name}</title>'
        f'<h1>Hello {name}</h1>'
        f'{"<p>".join(lorem_ipsum.paragraphs(3))}'
    ), name='hello'),
]
