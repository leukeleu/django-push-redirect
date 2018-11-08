from django.utils.http import is_safe_url


class Http2ServerPushRedirectMiddleware:
    redirect_status_codes = {301, 302}

    def __init__(self, get_response):
        self.get_response = get_response

    def should_preload(self, request, response):
        return (
            request.is_secure
            and response.status_code in self.redirect_status_codes
            and hasattr(response, 'url')
            and not response.has_header('Link')
        )

    def __call__(self, request):
        response = self.get_response(request)
        if self.should_preload(request, response):
            url = response.url
            if is_safe_url(url, allowed_hosts={request.get_host()}, require_https=True):
                response['Link'] = f'<{url}>; rel=preload'
        return response
