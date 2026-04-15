
"""
Production settings that handle missing packages.
"""

import os
import sys

# Production flag
PRODUCTION = os.environ.get('RAILWAY') or os.environ.get('RENDER')

if PRODUCTION:
    print("Running in production mode...", file=sys.stderr)
    
    # Ensure required settings
    DEBUG = False
    ALLOWED_HOSTS = ['*']  # Will be updated by Railway
    
    # List of packages to check
    packages_to_check = [
        ('django_browser_reload', 'django-browser-reload'),
        ('django_htmx', 'django-htmx'),
    ]
    
    # Check and remove missing packages
    for app_name, package_name in packages_to_check:
        if app_name in INSTALLED_APPS:
            try:
                __import__(app_name)
                print(f"✓ {package_name} is installed", file=sys.stderr)
            except ImportError:
                INSTALLED_APPS.remove(app_name)
                print(f"✗ {package_name} not installed, removing {app_name}", file=sys.stderr)
    
    # Add Railway-specific settings
    if 'RAILWAY' in os.environ:
        # Get Railway URL
        import socket
        hostname = socket.gethostname()
        ALLOWED_HOSTS = [hostname, '.railway.app', 'localhost', '127.0.0.1']
        
        # Database configuration
        if 'DATABASE_URL' in os.environ:
            import dj_database_url
            DATABASES = {
                'default': dj_database_url.config(
                    default=os.environ.get('DATABASE_URL'),
                    conn_max_age=600,
                    conn_health_checks=True,
                )
            }
            
        # Static files
        STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        
        # Add whitenoise middleware if not present
        if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
            MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
