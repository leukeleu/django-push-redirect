from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.utils.http import url_has_allowed_host_and_scheme


class Http2ServerPushRedirectMiddleware:
    redirect_status_codes = {301, 302, 303, 307, 308}

    def __init__(self, get_response):
        if not settings.SECURE_PROXY_SSL_HEADER:
            # For Django to be able to detect if a request is secure
            # some configuration is required, e.g..
            #
            # The nginx proxy should set:
            #
            #   proxy_set_header X-Forwarded-Proto $scheme;
            #
            # The Django project should set:
            #
            #   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
            raise MiddlewareNotUsed("SECURE_PROXY_SSL_HEADER is not configured")
        self.get_response = get_response

    def should_preload(self, request, response):
        if not getattr(response, "allow_push_redirect", True):
            # This response has explicitly opted out of push redirects
            return False

        if not request.is_secure():
            # HTTP/2 requires SSL/TLS.
            return False

        if not request.method == "GET":
            # Err on the side of caution by only preloading GET requests
            return False

        if response.status_code not in self.redirect_status_codes:
            # Not a redirect
            return False

        if not hasattr(response, "url"):
            # The url attribute is added by the HttpResponseRedirectBase
            # base class. This response does not have it so ignore it.
            return False

        if response.has_header("Link"):
            # There already is a Link header, don't overwrite it
            return False

        # Preload is enabled if the redirect url is on the same host
        # as the request and using the same protocol (https)
        return url_has_allowed_host_and_scheme(
            response.url, allowed_hosts={request.get_host()}, require_https=True
        )

    def __call__(self, request):
        response = self.get_response(request)
        if self.should_preload(request, response):
            # Response can be preloaded, add Link header
            response["Link"] = f"<{response.url}>; as=document; rel=preload"
        return response
