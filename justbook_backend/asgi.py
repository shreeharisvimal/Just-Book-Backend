# """
# ASGI config for justbook_backend project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from booking_management import routing	



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justbook_backend.settings')



# application = ProtocolTypeRouter({
# 	'http': get_asgi_application(),
# 	'websocket': AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
# })



import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import booking_management.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justbook_backend.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            booking_management.routing.websocket_urlpatterns
        )
    ),
})
