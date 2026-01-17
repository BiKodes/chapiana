"""
WSGI config for chapiana project.

It exposes the WSGI callable as a module-level variable named ``application``.

"""

import os

DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()

SETTINGS_MAP = {
    "local": "src.config.local",
    "production": "src.config.production",
}

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", SETTINGS_MAP.get(DJANGO_ENV, "src.config.local")
)
os.environ.setdefault("DJANGO_CONFIGURATION", DJANGO_ENV.capitalize())

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
