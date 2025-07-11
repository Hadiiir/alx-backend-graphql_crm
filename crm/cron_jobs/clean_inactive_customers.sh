#!/bin/bash

# Get script directory using BASH_SOURCE and pwd
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_DIR="$SCRIPT_DIR/../.."  # Adjust path to your project root

# Store current working directory
CWD=$(pwd)

# Change to project directory
cd "$PROJECT_DIR" || {
    echo "Failed to change to project directory" >> /tmp/customer_cleanup_log.txt
    exit 1
}

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

# Return to original directory
cd "$CWD" || exit