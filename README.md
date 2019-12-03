# Django HTTP/2 Server Push redirects

A Django middleware that adds a HTTP/2 Server Push header to plain
Django redirect responses.

This approach requires Django to be proxied by a server with
HTTP/2 Server Push support. E.g. `nginx>=1.3.9`, `apache2>=2.4.26` with 
`mod_http2` enabled or a CDN services like Cloudflare.

## Configuration

First configure your webserver to enable HTTP/2 and enable server push.

This looks something like this for nginx: 

```nginx
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  ...

  location @python {
    proxy_set_header X-Forwarded-Proto $scheme;
    http2_push_preload on;
    ...
  }
}
```

The configuration for Apache and other servers/services is left as an
exercise for the reader ;-).

Now make sure Django is able to detect if a request is secure 
by configuring the `SECURE_PROXY_SSL_HEADER` setting, e.g.:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
``` 

Then add `'push_redirect.middleware.Http2ServerPushRedirectMiddleware'`
to your project's `MIDDLEWARE`, making sure it's **before** Django's
`CommonMiddleware`:

```python
MIDDLEWARE = [
    ...
    'push_redirect.middleware.Http2ServerPushRedirectMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

This middleware adds the `Link rel=preload` header to redirect
responses that should be preloaded.

If everything is configured correctly you should see that redirects
no longer require an extra request the the webserver.

## Inspiration / References

* <https://twitter.com/simonw/status/1047865898717966337>
* <https://www.ctrl.blog/entry/http2-push-redirects>
* <https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/>
* <https://httpd.apache.org/docs/2.4/howto/http2.html#push>
* <https://www.cloudflare.com/website-optimization/http2/serverpush/>
* <https://code.djangoproject.com/ticket/29925>
