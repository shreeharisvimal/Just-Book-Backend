from celery import shared_task
from .models import Show
from django.utils import timezone
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def UpdateWebsocket(id, seatAllocation):

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'show_{id}',
        {
            'type':f"seat_update",
            'seat_data':seatAllocation,
        }
    )


@shared_task(bind=True)
def Check_Shows(self):
    current_time = str(timezone.now().time())
    current_date = str(timezone.now().date())
    shows = Show.objects.filter(Q(show_date__gt=current_date) | Q(show_date=current_date, show_time__gt=current_time))
    for show in shows:
        show.is_over = True
        show.save()
    return "Done"


@shared_task(bind=True)
def ShowSeatsUpdate(self):
    shows = Show.objects.all()
    for show in shows:
        seat_allocation = show.seatAllocation
        updated_seat_allocation = {}

        for key, row in seat_allocation.items():
            updated_seat_allocation[key] = {
                'type': row['type'],
                'seats': {
                    seat_num: {
                        'name': seat['name'],
                        'user': '',
                        'status': 'available',
                        'holdedseat': False,
                        'is_freeSpace': seat['is_freeSpace']
                    } for seat_num, seat in row['seats'].items()
                },
                'is_row_freeSpace': row['is_row_freeSpace']
            }

        UpdateWebsocket(show.id, updated_seat_allocation)
    
    return 'Done'

