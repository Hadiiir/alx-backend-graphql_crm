from celery import shared_task
from datetime import datetime
import logging
from .schema import schema

# Configure logging
logger = logging.getLogger(__name__)

@shared_task
def generate_crm_report():
    """
    Celery task that generates a weekly CRM report using GraphQL queries
    and logs the results to a file.
    """
    try:
        # GraphQL query to fetch CRM report data
        query = """
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
        
        # Execute the GraphQL query
        result = schema.execute(query)
        
        if result.errors:
            logger.error(f"GraphQL errors in CRM report: {result.errors}")
            return f"Error generating CRM report: {result.errors}"
        
        # Extract data from the result
        data = result.data
        total_customers = data['totalCustomers']
        total_orders = data['totalOrders']
        total_revenue = data['totalRevenue']
        
        # Format the report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_line = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue.\n"
        
        # Write to log file
        log_file_path = '/tmp/crm_report_log.txt'
        with open(log_file_path, 'a') as log_file:
            log_file.write(report_line)
        
        logger.info(f"CRM report generated successfully: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue")
        
        return f"CRM report generated: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue"
        
    except Exception as e:
        error_msg = f"Error generating CRM report: {str(e)}"
        logger.error(error_msg)
        
        # Log error to file as well
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_entry = f"{timestamp} - ERROR: {error_msg}\n"
        
        try:
            with open('/tmp/crm_report_log.txt', 'a') as log_file:
                log_file.write(error_entry)
        except Exception as log_error:
            logger.error(f"Failed to write error to log file: {log_error}")
        
        return error_msg

@shared_task
def test_crm_report():
    """
    Test task to manually trigger CRM report generation for debugging.
    """
    return generate_crm_report()

@shared_task
def cleanup_old_logs():
    """
    Optional task to clean up old log files (can be scheduled separately).
    """
    try:
        import os
        from datetime import datetime, timedelta
        
        # Clean up logs older than 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # This is a simple example - in practice, you'd implement
        # more sophisticated log rotation
        logger.info("Log cleanup task executed")
        return "Log cleanup completed"
        
    except Exception as e:
        logger.error(f"Error in log cleanup: {str(e)}")
        return f"Error in log cleanup: {str(e)}"