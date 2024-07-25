from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/seats/<int:show_id>/', consumers.SeatConsumer.as_asgi()),
]