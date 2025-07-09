from functools import wraps
from django.db.utils import OperationalError
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def database_required(view_func):
    """
    Decorator that checks database connectivity before executing the view
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return view_func(request, *args, **kwargs)
        except OperationalError as e:
            logger.error(f"Database connection failed in {view_func.__name__}: {e}")
            return handle_database_error(request, e)
        except Exception as e:
            # Check if it's a database-related error
            if any(keyword in str(e).lower() for keyword in ['connection', 'server', 'database']):
                logger.error(f"Database connection failed in {view_func.__name__}: {e}")
                return handle_database_error(request, e)
            # Re-raise non-database errors
            raise
    return wrapper


def handle_database_error(request, error):
    """
    Handle database connection errors with user-friendly response
    """
    context = {
        'error_type': 'Database Connection Error',
        'error_message': 'Unable to connect to the database. Please try again later.',
        'suggestion': 'This is usually a temporary issue. Please refresh the page or try again in a few moments.',
        'technical_details': str(error),
    }
    
    try:
        return render(request, 'feedback/error.html', context, status=503)
    except:
        # Fallback to simple HTTP response if template rendering fails
        return HttpResponse(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Database Connection Error</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 50px; background-color: #f8f9fa; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .error-icon { color: #dc3545; font-size: 48px; }
                    .btn { display: inline-block; padding: 10px 20px; margin: 10px 5px; text-decoration: none; border-radius: 5px; }
                    .btn-primary { background-color: #007bff; color: white; }
                    .btn-secondary { background-color: #6c757d; color: white; }
                    .alert { padding: 15px; margin: 20px 0; border-radius: 5px; background-color: #fff3cd; border: 1px solid #ffeaa7; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="error-icon">⚠️</div>
                    <h1>Database Connection Error</h1>
                    <div class="alert">
                        <p><strong>Unable to connect to the database.</strong></p>
                        <p>This is usually a temporary issue. Please try again in a few moments.</p>
                    </div>
                    <div>
                        <a href="/" class="btn btn-primary">Return to Home</a>
                        <a href="javascript:window.location.reload()" class="btn btn-secondary">Refresh Page</a>
                    </div>
                </div>
            </body>
            </html>
            """,
            status=503,
            content_type='text/html'
        )
