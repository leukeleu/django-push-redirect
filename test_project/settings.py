SECRET_KEY = 'not-that-secret'

import os

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = []

MIDDLEWARE = [
    'push_redirect.middleware.Http2ServerPushRedirectMiddleware',  # Must come first to rewrite the response of CommonMiddleware
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }
]

WSGI_APPLICATION = 'test_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    }
}

# Trust proxy headers

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
