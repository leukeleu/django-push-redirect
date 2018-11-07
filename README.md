# Django HTTP/2 Server Push redirects

This is a simple test project to try HTTP/2 Server Push redirects
with Django and nginx.


## Setup

This is a `docker-compose` project, do you'll need to download and
install [Docker Desktop](https://www.docker.com/products/docker-desktop)
to try this.


### Certificates

In order to use HTTP/2 it is required to get a certificate.

I personally recommend to use [`minica`](https://github.com/jsha/minica)
to generate a root CA cert and a cert for localhostL

    minica -domains localhost

Then add the generated root CA file to your OS/browsers trust store
and move the certs for `localhost` to `./conf/certs`.

The expected filenames for the certs are `cert.pem` and `cert.key`.


## Run the project

Once you've set up the certificates you should be able to start
nginx and Django using:

    docker-compose up -d
    
By visiting the following urls in a modern browser you should see the 
difference between "normal" redirects and HTTP/2 Server Push redirects:

* <http://localhost/hello/world> redirects to <http://localhost/hello/world/>
* <https://localhost/hello/world> redirects to and pushes <https://localhost/hello/world/>


### Code

The important nginx bit is in `conf/nginx/default.conf`:

    server {
      ...
    
      location @python {
        ...
        http2_push_preload on;
      }
    }


The important Django bit is in `push_redirect/http.py`:

    from django.http import HttpResponsePermanentRedirect

    class Http2PushPermanentRedirect(HttpResponsePermanentRedirect):
        def __init__(self, redirect_to, *args, **kwargs):
            super().__init__(redirect_to, *args, **kwargs)
            self['Link'] = f'<{self.url}>; rel=preload'

This subclass of `HttpResponsePermanentRedirect` adds a second
header that's used by nginx to push te resource.

This subclass is used as the redirect class in `CommonMiddleware`.


## Inspiration

* <https://twitter.com/simonw/status/1047865898717966337>
* <https://www.ctrl.blog/entry/http2-push-redirects>
* <https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/>
* <https://code.djangoproject.com/ticket/29925>
