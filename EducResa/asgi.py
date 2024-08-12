"""
ASGI config for EducResa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from channels.security.websocket import AllowedHostsOriginValidator # type: ignore
from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EducResa.settings')

# application = get_asgi_application()

asgi_application = get_asgi_application() # pour le protocole http uniquement

import chat.routing #new

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
            )})
