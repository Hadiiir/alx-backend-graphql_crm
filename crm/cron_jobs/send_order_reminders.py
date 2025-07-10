#!/usr/bin/env python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import os

# GraphQL endpoint configuration
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    use_json=True,
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=True,
)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GraphQL query to get recent orders
query = gql("""
    query GetRecentOrders($since: String!) {
        orders(filter: {order_date_gt: $since}) {
            id
            customer {
                email
            }
            order_date
            status
        }
    }
""")

try:
    # Execute the query
    result = client.execute(query, variable_values={"since": seven_days_ago})
    
    # Log results
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('/tmp/order_reminders_log.txt', 'a') as log_file:
        for order in result['orders']:
            log_entry = f"[{timestamp}] Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            log_file.write(log_entry)
    
    print("Order reminders processed!")
    
except Exception as e:
    with open('/tmp/order_reminders_log.txt', 'a') as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {str(e)}\n")
    print(f"Error processing order reminders: {e}")