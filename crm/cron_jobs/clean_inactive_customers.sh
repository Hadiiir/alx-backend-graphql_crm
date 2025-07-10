#!/bin/bash

# Set the working directory using BASH_SOURCE and pwd
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to Django project root
if [ -f "$SCRIPT_DIR/../manage.py" ]; then
    cd "$SCRIPT_DIR/.."
    CURRENT_DIR=$(pwd)
    echo "Current directory: $CURRENT_DIR" >> /tmp/customer_cleanup_log.txt
else
    echo "Error: Could not find manage.py" >> /tmp/customer_cleanup_log.txt
    exit 1
fi

# Execute the cleanup command
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer
from orders.models import Order

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    last_order_date__lt=one_year_ago
) | Customer.objects.filter(
    orders__isnull=True
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log results
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
if [ -z "$DELETED_COUNT" ]; then
    echo "[$TIMESTAMP] Error: No count received" >> /tmp/customer_cleanup_log.txt
else
    echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers." >> /tmp/customer_cleanup_log.txt
fi