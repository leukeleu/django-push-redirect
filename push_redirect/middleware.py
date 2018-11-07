from django.middleware.common import CommonMiddleware as DjangoCommonMiddleware

from .http import Http2ServerPushPermanentRedirect


class CommonMiddleware(DjangoCommonMiddleware):
    response_redirect_class = Http2ServerPushPermanentRedirect
