
import os

# Ensure these settings exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Update _core/settings.py with production settings
with open('_core/settings.py', 'a') as f:
    f.write('\n\n# Production settings for Railway\n')
    f.write('import os\n')
    f.write('import dj_database_url\n')
    f.write('\n')
    f.write('# Database\n')
    f.write('if "DATABASE_URL" in os.environ:\n')
    f.write('    DATABASES = {\n')
    f.write('        "default": dj_database_url.config(\n')
    f.write('            default=os.environ.get("DATABASE_URL"),\n')
    f.write('            conn_max_age=600,\n')
    f.write('            conn_health_checks=True,\n')
    f.write('        )\n')
    f.write('    }\n')
    f.write('\n')
    f.write('# Static files\n')
    f.write('STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")\n')
    f.write('STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"\n')
    f.write('\n')
    f.write('# Security\n')
    f.write('if "RAILWAY" in os.environ:\n')
    f.write('    DEBUG = False\n')
    f.write('    ALLOWED_HOSTS = ["*"]\n')
    f.write('    # Add whitenoise middleware\n')
    f.write('    if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:\n')
    f.write('        MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")\n')
