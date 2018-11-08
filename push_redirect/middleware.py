from django.utils.http import is_safe_url


class Http2ServerPushRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.is_secure and response.status_code in {301, 302} and hasattr(response, 'url'):
            url = response.url
            if is_safe_url(url, allowed_hosts={request.get_host()}, require_https=True):
                response['Link'] = f'<{url}>; rel=preload'
        return response
