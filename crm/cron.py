from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os

def get_graphql_client():
    """Shared function to create GraphQL client"""
    return Client(
        transport=RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            use_json=True,
        ),
        fetch_schema_from_transport=True,
    )

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    log_message = f"{timestamp} CRM is alive"
    
    # Write to log file
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(log_message + '\n')
    
    # Optional GraphQL health check
    try:
        client = get_graphql_client()
        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"GraphQL response: {result}\n")
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"GraphQL check failed: {str(e)}\n")

def update_low_stock():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        client = get_graphql_client()
        
        # Define and execute the mutation
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    products {
                        name
                        stock
                    }
                    message
                }
            }
        """)
        result = client.execute(mutation)
        
        # Log results
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"\n[{timestamp}] Stock Update Results:\n")
            f.write(f"Message: {result['updateLowStockProducts']['message']}\n")
            for product in result['updateLowStockProducts']['products']:
                f.write(f"Product: {product['name']}, New Stock: {product['stock']}\n")
    
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"\n[{timestamp}] Error: {str(e)}\n")