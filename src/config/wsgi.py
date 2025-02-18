"""
WSGI config for chapiana project.

It exposes the WSGI callable as a module-level variable named ``application``.

"""
import os

# Default to local environment if not explicitly set
DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()

# Map environments to config modules
SETTINGS_MAP = {
    "local": "config.local",
    "production": "config.production",
}

# Set the correct config module based on DJANGO_ENV
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MAP.get(DJANGO_ENV, "config.local"))
os.environ.setdefault("DJANGO_CONFIGURATION", DJANGO_ENV.capitalize())

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
