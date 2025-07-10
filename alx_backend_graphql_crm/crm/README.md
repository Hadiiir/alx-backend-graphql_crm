# CRM Celery Setup Guide

## Requirements
- Redis server
- Python dependencies

## Installation
1. Install Redis:
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

2. Install Python packages:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

## Running Celery
1. Start Celery worker:
```bash
celery -A crm worker -l info
```

2. Start Celery Beat (scheduler):
```bash
celery -A crm beat -l info
```

## Verification
Check report logs:
```bash
cat /tmp/crm_report_log.txt
```
