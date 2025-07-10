INSTALLED_APPS = [
    # ... other apps ...
    'django_crontab',
    'django_filters',
    'django_crontab',
    'graphene_django',
    'crm', 
    'django_celery_beat',

]

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TIMEZONE = 'UTC'

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat')
]

CRONJOBS = [
    # ... your existing cron jobs ...
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}