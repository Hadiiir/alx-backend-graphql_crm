#!/bin/bash

# Get current working directory
CWD=$(dirname "$0")
FULL_PATH="$CWD/../../"

# Activate virtual environment if exists
if [ -f "$FULL_PATH/venv/bin/activate" ]; then
    source "$FULL_PATH/venv/bin/activate"
else
    echo "Virtual environment not found. Proceeding without it." >> /tmp/customer_cleanup_log.txt
fi

# Execute Django shell command
OUTPUT=$(python "$FULL_PATH/manage.py" shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(last_order__lte=year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the results
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Deleted $OUTPUT inactive customers" >> /tmp/customer_cleanup_log.txt