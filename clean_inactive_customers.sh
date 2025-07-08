#!/bin/bash

# Get the current date and time for logging
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Execute the Django command to delete inactive customers and capture output
OUTPUT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer
from orders.models import Order

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    last_order_date__lt=one_year_ago
) | Customer.objects.filter(
    last_order_date__isnull=True,
    date_joined__lt=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result
echo "[$TIMESTAMP] Deleted $OUTPUT inactive customers" >> /tmp/customer_cleanup_log.txt