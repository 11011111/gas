import os

# Корневая директория проекта
# Пример использованя: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Секретный ключ
SECRET_KEY = 'nv=_bi35g($0u0)sftrfvwcimw3fc-@_a00l+vej(t7vm9)_kw'

# Режим тестрования
DEBUG = True

# Переназначение базовой модели пользователя Django
AUTH_USER_MODEL = 'person.User'

# Массив с которых доступен сервис
ALLOWED_HOSTS = ['*']

# Установленные приложения django и собственные приложения
INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gas.pages',
    'gas.person',
    'gas.api',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'request_logging.middleware.LoggingMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',  # change debug level as appropiate
            'propagate': False,
        },
    },
}

ROOT_URLCONF = 'gas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gas.wsgi.application'

# Настройка БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gas_db',
        'USER': 'gas_db_user',
        'PASSWORD': 'gas_db_password',
        'HOST': 'localhost',
        'PORT': '54312',
    },
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'gasgoldvkr@gmail.com'
EMAIL_HOST_PASSWORD = '24936mega'
EMAIL_CODE_PERIOD = 24*60*60

# Параметры локализации, интернационализации
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Параметры статики и медиафайлов
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
LOGIN_URL = '/auth/login/'
# Настройки DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

HOST_URL = 'http://0.0.0.0:8002/'

BAD_PASSWORD_MAX_COUNT = 5
BAD_PASSWORD_TIMEOUT = 24*60*60
