"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from chat.routing import ws_urlpatterns
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

django_application = get_asgi_application()
application = ProtocolTypeRouter({
    "http":django_application,
    "websocket":AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})
