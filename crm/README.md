# CRM Celery Setup Guide

## Prerequisites
- Redis server
- Python 3.6+
- Django

## Installation
1. Install dependencies:
```bash
sudo apt install redis-server
python3 -m pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start Redis:
```bash
sudo systemctl start redis
```

## Running Celery
1. Start Celery worker:
```bash
celery -A crm worker -l info
```

2. Start Celery Beat (for scheduled tasks):
```bash
celery -A crm beat -l info
```

## Verification
Check the report logs:
```bash
cat /tmp/crm_report_log.txt
```

The report will be generated every Monday at 6:00 AM.