from celery import shared_task
from .models import Show
from django.db.models import Q
from django.utils import timezone


@shared_task(bind=True)
def Check_Shows(self):
    current_time, current_date = str(timezone.now().time()), str(timezone.now().date())
    shows = Show.objects.filter(Q(show_date__gt=current_date) | Q(show_date=current_date, show_time__gt=current_time))
    for show in shows:
        show.is_over = True
        show.save()
    return "Done"

