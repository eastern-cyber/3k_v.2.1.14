
import os
import sys
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
try:
    import django
    django.setup()
    print("✅ Django setup successful")
    from django.core.management import execute_from_command_line
    print("✅ Django management commands available")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)
