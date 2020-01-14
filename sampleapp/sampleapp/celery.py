import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleapp.settings')

app = Celery('sampleapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.task
def test():
    print("RUN........")
