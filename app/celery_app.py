from celery import Celery
from celery.schedules import crontab

celery_app = Celery('app', 
                    broker='redis://redis_container:6379/0', 
                    backend='redis://redis_container:6379/0')

celery_app.conf.timezone = 'Europe/Kyiv'


celery_app.conf.beat_schedule = {
    'test-every-three-minutes': {
        'task': 'reduce_hp_task', 
        'schedule': crontab(hour=0, minute=0), 
    },
    'reset-progress-weekly': {
        'task': 'reset_progress_task', 
        'schedule': crontab(day_of_week=1, hour=0, minute=0),
    },
}

"""
CODE FOR TESTING CELERY TASKS EVERY THREE MINUTES
"""

# celery_app.conf.beat_schedule = {
#     'test-every-three-minutes': {
#         'task': 'reduce_hp_task', 
#         'schedule': crontab(minute='*/3'),
#     },
#     'reset-progress-weekly': {
#         'task': 'reset_progress_task', 
#         'schedule': crontab(minute='*/3'),
#     },
# }
celery_app.autodiscover_tasks(['app'], related_name='celery_tasks')