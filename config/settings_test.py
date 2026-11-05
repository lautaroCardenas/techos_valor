from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'techos_valor_test',
        'USER': 'postgres',
        'PASSWORD': '1996',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'prefer'},
    }
}