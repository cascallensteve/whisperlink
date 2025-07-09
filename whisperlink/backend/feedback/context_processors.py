from django.contrib.auth.models import AnonymousUser
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)


def safe_user_context(request):
    """
    Context processor that provides additional safe user context
    and database connectivity status
    """
    try:
        # Try to test database connectivity
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_available = True
    except OperationalError as e:
        logger.error(f"Database error in context processor: {e}")
        db_available = False
    except Exception as e:
        # Check if it's a database-related error
        if any(keyword in str(e).lower() for keyword in ['connection', 'server', 'database']):
            logger.error(f"Database error in context processor: {e}")
            db_available = False
        else:
            db_available = True
    
    return {
        'db_available': db_available,
        'is_database_connected': db_available,
    }
