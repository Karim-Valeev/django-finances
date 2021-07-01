import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finances.settings")

app = Celery("finances")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(packages=["app"])
