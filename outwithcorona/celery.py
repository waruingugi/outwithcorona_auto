from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outwithcorona.settings')

app = Celery('outwithcorona')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # name of the scheduler
    "get-latest-stat-for-kenya": {
        # task name which we have created in tasks.py
        'task': 'get_latest_stat_for_kenya',

        # execute twice a day
        'schedule': crontab(minute=0, hour='*/1')
    }

}
