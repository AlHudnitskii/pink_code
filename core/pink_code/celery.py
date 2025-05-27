import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.pink_code.settings')

app = Celery('pink_code')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()