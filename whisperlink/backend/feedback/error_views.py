from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound


def handler404(request, exception):
    """Custom 404 error handler"""
    context = {
        'error_type': 'Page Not Found',
        'error_message': 'The page you requested could not be found.',
        'suggestion': 'Please check the URL and try again, or use the navigation links to find what you\'re looking for.',
        'technical_details': f'Path: {request.path}',
    }
    return render(request, 'feedback/error.html', context, status=404)


def handler500(request):
    """Custom 500 error handler"""
    context = {
        'error_type': 'Internal Server Error',
        'error_message': 'Something went wrong on our end. We\'re working to fix it.',
        'suggestion': 'Please try again later. If the problem persists, contact support.',
        'technical_details': 'The server encountered an internal error and could not complete your request.',
    }
    return render(request, 'feedback/error.html', context, status=500)


def handler403(request, exception):
    """Custom 403 error handler"""
    context = {
        'error_type': 'Access Forbidden',
        'error_message': 'You don\'t have permission to access this resource.',
        'suggestion': 'Please log in or contact support if you believe this is an error.',
        'technical_details': f'Path: {request.path}',
    }
    return render(request, 'feedback/error.html', context, status=403)
