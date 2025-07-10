#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the Django project root directory (assuming it's one level up from cron_jobs)
cd "$SCRIPT_DIR/.."

# Execute the Python command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer
from orders.models import Order

# Calculate the date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
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

# Log the result with timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers." >> /tmp/customer_cleanup_log.txt