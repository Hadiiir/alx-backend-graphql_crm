#!/bin/bash

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR="$DIR/../.."  # Adjust if your structure is different

# Activate virtual environment if exists
if [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
fi

# Execute Django shell command
OUTPUT=$(python "$PROJECT_DIR/manage.py" shell -c "
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