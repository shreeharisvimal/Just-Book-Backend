from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justbook_backend.settings')

app = Celery('justbook_backend')
app.config_from_object('django.conf:settings', namespwace='CELERY')
app.autodiscover_tasks()

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata',
	    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
	    beat_schedule={
                    'Show_Update_task': {
                        'task': 'show_management.tasks.Check_Shows',
                        'schedule': crontab(hour=0, minute=0),
                    },
                    'seatsShowSeatsUpdate':{
                        'task': 'show_management.tasks.ShowSeatsUpdate',
                        'schedule': timedelta(minutes=5),
                    }
                },
	)

app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'


app.conf.task_serializer = 'json'
app.conf.timezone = 'Asia/Kolkata'
app.conf.accept_content = ['json']
app.conf.result_serializer = 'json'
app.conf.broker_connection_retry_on_startup = True
app.conf.cache_backend = 'default'
