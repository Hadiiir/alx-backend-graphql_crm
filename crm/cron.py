import os
import django
from datetime import datetime
from graphene.test import Client
from django.conf import settings
from .schema import schema

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def update_low_stock():
    # Create GraphQL client
    client = Client(schema)
    
    # Execute the mutation
    mutation = '''
    mutation {
        updateLowStockProducts {
            products {
                id
                name
                stock
            }
            message
        }
    }
    '''
    result = client.execute(mutation)
    
    # Log the results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        f.write(f"[{timestamp}] Stock Update Results:\n")
        if 'errors' in result:
            f.write(f"Error: {result['errors']}\n")
        else:
            data = result['data']['updateLowStockProducts']
            f.write(f"Message: {data['message']}\n")
            for product in data['products']:
                f.write(f"Updated {product['name']} to stock {product['stock']}\n")
            f.write("\n")