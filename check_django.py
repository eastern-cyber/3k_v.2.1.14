
#!/usr/bin/env python
import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Try to setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')

try:
    import django
    django.setup()
    print("✅ Django setup successful")
    
    # Check installed apps
    from django.conf import settings
    print(f"\n📋 INSTALLED_APPS ({len(settings.INSTALLED_APPS)} apps):")
    for app in settings.INSTALLED_APPS:
        print(f"  - {app}")
    
    # Check database
    print(f"\n🗄️ Database engine: {settings.DATABASES['default']['ENGINE']}")
    
    # Check middleware
    print(f"\n🛡️ MIDDLEWARE ({len(settings.MIDDLEWARE)} items):")
    for mw in settings.MIDDLEWARE[:5]:  # First 5 only
        print(f"  - {mw}")
    
    print("\n🎉 All checks passed!")
    
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
