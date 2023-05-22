import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Если ваше основное приложение - news, используйте следующую строку:
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-weekly-digest': {
        'task': 'news.tasks.weekly_digest',
        'schedule': crontab(day_of_week='monday', hour=8)
    }
}