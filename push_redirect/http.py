from django.http import HttpResponsePermanentRedirect


class Http2PushPermanentRedirect(HttpResponsePermanentRedirect):
    def __init__(self, redirect_to, *args, **kwargs):
        super().__init__(redirect_to, *args, **kwargs)
        self['Link'] = f'<{self.url}>; rel=preload'
