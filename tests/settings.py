import os

SECRET_KEY = "not-that-secret"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = []

MIDDLEWARE = [
    # Must come first to rewrite the response of CommonMiddleware
    "push_redirect.middleware.Http2ServerPushRedirectMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates"}]

WSGI_APPLICATION = "tests.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.path.dirname(__file__), "db.sqlite3"),
    }
}

# Trust proxy headers

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
