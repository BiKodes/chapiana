import os
from datetime import timedelta
from os.path import join


import environ
from configurations import Configuration
from django.utils.crypto import get_random_string
from kombu import Exchange, Queue
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    env = environ.Env()

    INSTALLED_APPS = (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        
        # Third party apps
        "rest_framework",
        "rest_framework.authtoken",
        # "django_filters",
        # "rest_framework_simplejwt",
        # "rest_framework_simplejwt.token_blacklist",
        # "drf_yasg",
        # "corsheaders",
        "configurations",

        # Custom apps
        "src.accounts.apps.AccountsConfig",
        "src.chat.apps.ChatConfig",
    )


    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    )

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",
        "http://127.0.0.1:9000",
    ]

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = "src.config.urls"
    SECRET_KEY = env("DJANGO_SECRET_KEY")
    WSGI_APPLICATION = "src.wsgi.application"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    ADMINS = (("Author", "bikocodes@gmail.com"),)

    
    DATABASES = {
       'default': {
           "NAME": env.str("POSTGRES_NAME"),
            "USER": env.str("POSTGRES_USER"),
            "PASSWORD":env.str ("POSTGRES_PASSWORD"),
            "HOST": env.str("POSTGRES_HOST", "localhost"),
            "PORT": env.int("POSTGRES_PORT", 5432),
            "ENGINE": "django.db.backends.postgresql",
            # "ATOMIC_REQUEST": True,
            # "OPTIONS": {
            #     "server_side_binding": True,
            #     "isolation_level": ISOLATION_LEVEL_READ_COMMITTED
            # }
        }
    }

    # Enable Connection Pooling
    # DATABASES['default']['ENGINE'] = 'django_postgrespool'

    APPEND_SLASH = False
    TIME_ZONE = "UTC"
    LANGUAGE_CODE = "en-us"

    # If you set this to False, Django will make some optimizations so 
    # as not to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = "/"

    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    SECRET_KEY = get_random_string(50, chars)

    # Static files (CSS, JavaScript, Images)
  
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
    STATICFILES_DIRS = []
    STATIC_URL = "/static/"
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
    MEDIA_URL = "/media/"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": STATICFILES_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    DEBUG = env.bool("DJANGO_DEBUG", False)

    # Password Validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["mail_admins", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {"handlers": ["console"], "level": "INFO"},
        },
    }

    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": env.int("DJANGO_PAGINATION_LIMIT", 10),
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        "DEFAULT_RENDERER_CLASSES": (
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ),
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ),
    }

    AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    }
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Nginx SSL
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/etc/nginx/ssl/cert.pem")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "/etc/nginx/ssl/key.pem")

    # Email Configs
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

    AUTH_USER_MODEL = 'accounts.ChapianaUser'

    # Celery
    CELERY_BROKER_URL = env.str("BROKER_URL", "redis://localhost:6379/0")
    RESULT_BACKEND = os.getenv("RESULT_BACKEND", CELERY_BROKER_URL)
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_DEFAULT_QUEUE = "chapiana_tasks"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_RESULT_EXPIRES = 300  # 5 minutes
    CELERY_TASK_HIGH_PRIORITY = 10
    CELERY_TASK_QUEUES = (
        Queue(
            CELERY_DEFAULT_QUEUE,
            Exchange(CELERY_DEFAULT_QUEUE),
            routing_key=CELERY_DEFAULT_QUEUE,
            queue_arguments={"x-max-priority": CELERY_TASK_HIGH_PRIORITY},
        ),
    )
    CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
