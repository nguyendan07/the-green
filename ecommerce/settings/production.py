from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_PRIVATE_KEY = config('STRIPE_PRIVATE_KEY')
