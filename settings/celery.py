import os
from celery import Celery
from .celery_apps import CELERY_APPS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("djangogirls")
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks(lambda: CELERY_APPS)