#!/bin/bash

# Execute the cleanup command directly without directory changes
DELETED_COUNT=$(python3 /path/to/your/project/manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer

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
echo "[$TIMESTAMP] Deleted ${DELETED_COUNT:-0} inactive customers." >> /tmp/customer_cleanup_log.txt