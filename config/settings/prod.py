from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email para producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
