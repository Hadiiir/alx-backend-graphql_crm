import os
import django
from datetime import datetime
from graphene.test import Client
from .schema import schema

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def update_low_stock():
    client = Client(schema)
    
    mutation = '''
    mutation {
        updateLowStockProducts {
            products {
                name
                stock
            }
            message
        }
    }
    '''
    
    result = client.execute(mutation)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        f.write(f"[{timestamp}] Stock Update:\n")
        if 'data' in result and result['data']['updateLowStockProducts']:
            data = result['data']['updateLowStockProducts']
            f.write(f"Message: {data['message']}\n")
            for product in data['products']:
                f.write(f"- {product['name']}: New stock {product['stock']}\n")
        else:
            f.write("Error in stock update mutation\n")
        f.write("\n")