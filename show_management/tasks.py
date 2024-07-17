from celery import shared_task
from .models import Show
# from datetime import date, datetime
from django.utils import timezone
from django.db.models import Q

@shared_task(bind=True)
def Check_Shows(self):
    current_time = str(timezone.now().time())
    current_date = str(timezone.now().date())
    shows = Show.objects.filter(Q(show_date__gt=current_date) | Q(show_date=current_date, show_time__gt=current_time))
    for show in shows:
        show.is_over = True
        show.save()
    return "Done"
