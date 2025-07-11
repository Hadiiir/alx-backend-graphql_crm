#!/bin/bash

# Store current working directory
cwd=$(pwd)

# Change to project directory
if cd /path/to/alx-backend-graphql_crm; then
    # Execute Django shell command
    OUTPUT=$(python manage.py shell -c "
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
else
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Failed to change directory" >> /tmp/customer_cleanup_log.txt
    exit 1
fi

# Return to original directory
cd "$cwd" || exit