# Error Handling System

This document explains the custom error handling system implemented in WhisperLink.

## Features

### 1. Database Connection Error Handling
- **Middleware**: `feedback.middleware.DatabaseErrorMiddleware`
- **Purpose**: Catches database connection errors and shows user-friendly messages
- **Error Types**: PostgreSQL/Supabase connection failures, timeouts, SSL errors
- **Response**: Custom error page with helpful suggestions

### 2. Custom Error Pages
- **404 (Not Found)**: Custom page for missing resources
- **500 (Internal Server Error)**: Friendly error page for server issues
- **403 (Forbidden)**: Access denied page
- **503 (Service Unavailable)**: Database connection issues

### 3. Health Check Endpoint
- **URL**: `/health/`
- **Purpose**: Test database connectivity
- **Response**: JSON with database status
- **Usage**: Monitor system health, troubleshoot connection issues

## Implementation Details

### Middleware Configuration
```python
MIDDLEWARE = [
    # ... other middleware ...
    'feedback.middleware.DatabaseErrorMiddleware',
]
```

### Custom Error Handlers
```python
# In main urls.py
handler404 = 'feedback.error_views.handler404'
handler500 = 'feedback.error_views.handler500'
handler403 = 'feedback.error_views.handler403'
```

### Error Template Features
- User-friendly error messages
- Suggested actions to resolve issues
- Navigation buttons (Home, Refresh, Contact)
- Health check link
- Technical details (expandable)
- Responsive design matching site theme

## Error Types Handled

### Database Connection Errors
- **Error**: `OperationalError: connection to server failed`
- **Cause**: Supabase/PostgreSQL connection issues
- **Response**: 503 Service Unavailable with retry suggestions
- **Logging**: Errors logged to `logs/error.log`

### Template Errors
- **Error**: `TemplateDoesNotExist: base.html`
- **Cause**: Missing template files
- **Response**: 500 Internal Server Error
- **Solution**: All templates now use `feedback/base.html`

### CSRF Errors
- **Error**: `Forbidden (CSRF token incorrect)`
- **Cause**: Invalid or missing CSRF tokens
- **Response**: 403 Forbidden with login suggestions

## Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'feedback.middleware': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Usage Examples

### Check System Health
```bash
curl http://localhost:8000/health/
```

Response:
```json
{
    "database": "connected",
    "status": "healthy"
}
```

### Database Connection Error
When database is unavailable:
```json
{
    "database": "error: connection to server failed",
    "status": "unhealthy"
}
```

## User Experience

Instead of Django's default error pages, users now see:
- Clear error explanations
- Actionable next steps
- Easy navigation options
- System status information
- Professional appearance matching the site design

## Monitoring

- Check `/health/` endpoint for system status
- Monitor `logs/error.log` for detailed error information
- Database connection issues are logged with full stack traces
- User-friendly pages prevent user confusion during outages

## Benefits

1. **Better User Experience**: Clear, helpful error messages
2. **Easier Troubleshooting**: Health check endpoint and detailed logging
3. **Professional Appearance**: Custom error pages match site design
4. **Reduced Support Load**: Users can understand and resolve many issues themselves
5. **System Monitoring**: Easy way to check database connectivity
