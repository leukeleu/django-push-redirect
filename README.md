# Django HTTP/2 Server Push redirects

This is a simple test project to try HTTP/2 Server Push redirects
with Django and nginx.

This approach requires nginx>=1.3.9


## Setup

This is a `docker-compose` project, download and install 
[Docker Desktop](https://www.docker.com/products/docker-desktop)
to run this.


### Certificates

In order to use HTTP/2 a certificate is required.

[`minica`](https://github.com/jsha/minica) is a excellent tool
to generate a root CA certificate and a certificate for `localhost`

    minica -domains localhost

Then add the generated root CA file to the OS/browsers trust store
and move the certificates for `localhost` to `./conf/certs`.

The expected file names for the certificates are `cert.pem` and `cert.key`.


## Run the project

Once the certificates have been set up, run nginx and Django using:

    docker-compose up -d
    
Visiting the following urls in a modern browser should show the 
difference between "normal" redirects and HTTP/2 Server Push redirects:

* <http://localhost/hello/world> redirects to <http://localhost/hello/world/>
* <https://localhost/hello/world> redirects to and pushes <https://localhost/hello/world/>


### Code

The most important bit of nginx configuration in `conf/nginx/default.conf` is:

    server {
      ...
    
      location @python {
        ...
        proxy_set_header X-Forwarded-Proto $scheme;
        ...
        http2_push_preload on;
      }
    }


The most important Python/Django code is in `push_redirect/middleware.py`:

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

This middleware adds the `Link rel=preload` header to redirect
responses. But only if the redirect url is safe (same host or relative)
and the request is secure.

This middleware must be place **before** `CommonMiddleware`.


## Inspiration

* <https://twitter.com/simonw/status/1047865898717966337>
* <https://www.ctrl.blog/entry/http2-push-redirects>
* <https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/>
* <https://code.djangoproject.com/ticket/29925>
