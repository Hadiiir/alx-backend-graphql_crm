CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

INSTALLED_APPS = [
    # ... other apps ...
    'django_crontab',
    'graphene_django',
]

GRAPHENE = {
    'SCHEMA': 'crm.schema.schema'
}
