from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            use_json=True,
        )
        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        query = gql("""
            query {
                totalCustomers
                totalOrders
                totalRevenue
            }
        """)

        result = client.execute(query)
        
        log_entry = (
            f"{timestamp} - Report: "
            f"{result['totalCustomers']} customers, "
            f"{result['totalOrders']} orders, "
            f"{result['totalRevenue']} revenue\n"
        )
        
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(log_entry)
            
        return log_entry

    except Exception as e:
        error_msg = f"{timestamp} - Report generation failed: {str(e)}\n"
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(error_msg)
        return error_msg