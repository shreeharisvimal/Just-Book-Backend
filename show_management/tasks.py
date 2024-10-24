from celery import shared_task
from .models import Show
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist


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

