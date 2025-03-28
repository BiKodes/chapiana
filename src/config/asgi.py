"""
ASGI config for chapiana project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""
import os
from channels.routing import ProtocolTypeRouter


# Default to local environment if not explicitly set
DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()

# Map environments to config modules
SETTINGS_MAP = {
    "local": "src.config.local",
    "production": "src.config.production",
}

# Set the correct config module based on DJANGO_ENV
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MAP.get(DJANGO_ENV, "src.config.local"))
os.environ.setdefault("DJANGO_CONFIGURATION", DJANGO_ENV.capitalize())

from configurations.asgi import get_asgi_application

application = ProtocolTypeRouter(
   { 
       "http": get_asgi_application(),
    
   }
)
