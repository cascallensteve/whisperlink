from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.db.utils import OperationalError
from django.template import TemplateDoesNotExist
import logging

logger = logging.getLogger(__name__)


class DatabaseErrorMiddleware:
    """
    Middleware to handle database connection errors gracefully
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except OperationalError as e:
            logger.error(f"Database connection error: {e}")
            return self.handle_database_error(request, e)
        except Exception as e:
            # Check if it's a database-related error in the exception chain
            if self.is_database_error(e):
                logger.error(f"Database connection error: {e}")
                return self.handle_database_error(request, e)
            raise

    def is_database_error(self, exception):
        """Check if an exception is related to database connectivity"""
        error_str = str(exception).lower()
        error_indicators = [
            'connection to server',
            'server closed the connection',
            'timeout while waiting',
            'scram exchange',
            'connection failed',
            'operationalerror',
            'database connection',
            'connection reset'
        ]
        
        # Check the current exception
        if any(indicator in error_str for indicator in error_indicators):
            return True
            
        # Check the exception chain
        current = exception
        while current.__cause__ or current.__context__:
            current = current.__cause__ or current.__context__
            if current and any(indicator in str(current).lower() for indicator in error_indicators):
                return True
                
        return False

    def handle_database_error(self, request, error):
        """
        Handle database connection errors with user-friendly message
        """
        context = {
            'error_type': 'Database Connection Error',
            'error_message': 'Unable to connect to the database. Please try again later.',
            'suggestion': 'This is usually a temporary issue. Please refresh the page or try again in a few moments.',
            'technical_details': str(error) if hasattr(error, '__str__') else 'Connection failed',
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
                        <h3>What you can do:</h3>
                        <ul>
                            <li>Refresh the page and try again</li>
                            <li>Check your internet connection</li>
                            <li>Wait a few moments and try again</li>
                            <li>Contact support if the problem persists</li>
                        </ul>
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
