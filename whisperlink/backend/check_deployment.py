#!/usr/bin/env python3
"""
Deployment Configuration Checker for WhisperLink
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whisperlink_backend.settings')

import django
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.test.utils import get_runner
import requests

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    
    required_vars = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER', 
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def check_database_connection():
    """Check database connectivity"""
    print("\n🗄️  Checking Database Connection...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_static_files():
    """Check static files configuration"""
    print("\n📁 Checking Static Files Configuration...")
    
    try:
        # Check if static root is configured
        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            print("❌ STATIC_ROOT is not configured")
            return False
        
        # Check if static URL is configured
        if not settings.STATIC_URL:
            print("❌ STATIC_URL is not configured")
            return False
        
        # Check if WhiteNoise is in middleware
        if 'whitenoise.middleware.WhiteNoiseMiddleware' not in settings.MIDDLEWARE:
            print("❌ WhiteNoise middleware is not configured")
            return False
        
        print("✅ Static files configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ Static files configuration error: {e}")
        return False

def check_security_settings():
    """Check security settings for production"""
    print("\n🔒 Checking Security Settings...")
    
    issues = []
    
    # Check DEBUG setting
    if settings.DEBUG:
        issues.append("DEBUG is set to True (should be False in production)")
    
    # Check SECRET_KEY
    if not settings.SECRET_KEY or settings.SECRET_KEY.startswith('django-insecure-'):
        issues.append("SECRET_KEY is not properly configured for production")
    
    # Check ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
        issues.append("ALLOWED_HOSTS should be configured with specific domains")
    
    if issues:
        print("⚠️  Security issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Security settings are properly configured")
        return True

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API Keys...")
    
    # Check Together AI API key
    if not settings.TOGETHER_API_KEY or settings.TOGETHER_API_KEY == 'your-together-api-key-here':
        print("⚠️  Together AI API key is not configured (AI features will not work)")
        return False
    else:
        print("✅ Together AI API key is configured")
        return True

def check_email_configuration():
    """Check email configuration"""
    print("\n📧 Checking Email Configuration...")
    
    if not os.getenv('EMAIL_HOST_USER') or not os.getenv('EMAIL_HOST_PASSWORD'):
        print("⚠️  Email configuration is not complete (password reset won't work)")
        return False
    else:
        print("✅ Email configuration is complete")
        return True

def run_django_checks():
    """Run Django's built-in system checks"""
    print("\n🔧 Running Django System Checks...")
    
    try:
        call_command('check', verbosity=0)
        print("✅ Django system checks passed")
        return True
    except Exception as e:
        print(f"❌ Django system checks failed: {e}")
        return False

def main():
    """Main deployment check function"""
    print("🚀 WhisperLink Deployment Configuration Check")
    print("=" * 50)
    
    checks = [
        check_environment_variables,
        check_database_connection,
        check_static_files,
        check_security_settings,
        check_api_keys,
        check_email_configuration,
        run_django_checks,
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your application is ready for deployment.")
        return True
    else:
        print("⚠️  Some checks failed. Please review the issues above before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
