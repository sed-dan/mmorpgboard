import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpgboard.settings')

app = Celery('mmorpgboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.update(
    CELERY_TIMEZONE='UTC',
    CELERYD_POOL='solo',
)

app.conf.beat_schedule = {
    'weekly_notification_at_monday_10am': {
        'task': 'board.tasks.weekly_notification_task',
        'schedule': crontab(minute=0, hour=10, day_of_week='monday'),
    },
}

app.conf.beat_schedule = {
    'clear-old-codes-every-10min': {
        'task': 'board.tasks.clear_old_codes',
        'schedule': crontab(minute='*/10'),
    },
}