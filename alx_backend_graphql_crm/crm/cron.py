from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_graphql_client():
    """Shared GraphQL client configuration"""
    return Client(
        transport=RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            use_json=True,
        ),
        fetch_schema_from_transport=True,
    )

def log_operation(file_path, message, mode='a'):
    """Shared logging function"""
    with open(file_path, mode) as f:
        f.write(message + '\n')

def log_crm_heartbeat():
    """Logs CRM heartbeat with optional GraphQL health check"""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    log_message = f"{timestamp} CRM is alive"
    log_operation('/tmp/crm_heartbeat_log.txt', log_message)
    
    # Optional GraphQL health check
    try:
        client = get_graphql_client()
        result = client.execute(gql("query { hello }"))
        log_operation('/tmp/crm_heartbeat_log.txt', 
                     f"GraphQL response: {result}")
    except Exception as e:
        log_operation('/tmp/crm_heartbeat_log.txt',
                     f"GraphQL check failed: {str(e)}")

def update_low_stock():
    """Updates low stock products and logs results"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        client = get_graphql_client()
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
        
        log_entry = f"\n[{timestamp}] Stock Update Results:\n"
        if result.get('updateLowStockProducts'):
            data = result['updateLowStockProducts']
            for product in data['products']:
                log_entry += f"Updated {product['name']} - New stock: {product['stock']}\n"
            log_entry += f"Status: {data['message']}\n"
        else:
            log_entry += "No products were updated\n"
        
        log_operation('/tmp/low_stock_updates_log.txt', log_entry)
    
    except Exception as e:
        error_msg = f"[{timestamp}] Error: {str(e)}"
        log_operation('/tmp/low_stock_updates_log.txt', error_msg)