from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.utils import lorem_ipsum


class CustomRedirectResponse(HttpResponse):
    status_code = 302

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["Location"] = "/custom-redirect/redirected/"


class CustomLinkResponse(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["Link"] = "<https://www.google.com/>; rel=preconnect"


def opt_out(request):
    response = HttpResponseRedirect("/")
    response.allow_push_redirect = False
    return response


urlpatterns = [
    path("", lambda request: HttpResponseRedirect(reverse("hello").rstrip("/"))),
    path("opt-out/", opt_out, name="opt-out"),
    path(
        "hello/",
        lambda request: HttpResponseRedirect(
            reverse("hello", kwargs={"name": "world"}).rstrip("/")
        ),
        name="hello",
    ),
    path(
        "hello/<slug:name>/",
        lambda request, name: HttpResponse(
            f"<!doctype html>"
            f"<title>Hello {name}</title>"
            f"<h1>Hello {name}</h1>"
            f'{"<p>".join(lorem_ipsum.paragraphs(1))}'
        ),
        name="hello",
    ),
    path(
        "custom-redirect/",
        lambda request: CustomRedirectResponse(),
        name="custom-redirect",
    ),
    path(
        "custom-link/",
        lambda request: CustomLinkResponse("https://www.google.com/"),
        name="custom-redirect",
    ),
    path(
        "google/",
        lambda request: HttpResponseRedirect("https://www.google.com/"),
        name="google",
    ),
]
