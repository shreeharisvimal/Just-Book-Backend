import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.apps import apps

class SeatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.show_id = self.scope['url_route']['kwargs']['show_id']
        print('This is the show id ', self.show_id)
        self.room_group_name = f'show_{self.show_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        seat_data = text_data_json['data']['seat_data']
        await self.save_seat_data(seat_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'seat_update',
                'seat_data': seat_data
            }
        )

    async def seat_update(self, event):
        seat_data = event['seat_data']
        await self.send(text_data=json.dumps({
            'seat_data': seat_data
        }))

    @database_sync_to_async
    def save_seat_data(self, seat_data):
        Show = apps.get_model('show_management', 'Show')
        try:
            show = Show.objects.get(id=self.show_id)
            show.seatAllocation = seat_data
            return show.save()
        except Show.DoesNotExist:
            pass