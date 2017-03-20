from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django_kids',                      # Or path to database file if using sqlite3.
        'USER': 'django_kids',                      # Not used with sqlite3.
        'PASSWORD': 'django_kids',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

INSTALLED_APPS += ('debug_toolbar',)
INTERNAL_IPS = ("127.0.0.1", "209.52.229.146", "192.168.1.10", "192.168.1.31")
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS':False}
MIDDLEWARE_CLASSES += \
    ("debug_toolbar.middleware.DebugToolbarMiddleware", )
