import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import booking_management.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justbook_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            booking_management.routing.websocket_urlpatterns
        )
    ),
})
