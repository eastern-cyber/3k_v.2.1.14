
#!/usr/bin/env python
"""
Minimal Django app for Railway deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
    
    try:
        django.setup()
        print("✅ Django initialized successfully")
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed")
        
        # Start server
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        
        import gunicorn.app.base
        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': f"0.0.0.0:{os.getenv('PORT', '8000')}",
            'workers': 1,
            'timeout': 120,
        }
        StandaloneApplication(application, options).run()
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
