
import os
import re

# Read settings.py
with open('_core/settings.py', 'r') as f:
    content = f.read()

# Find all INSTALLED_APPS
pattern = r"INSTALLED_APPS\s*=\s*\[(.*?)\]"
match = re.search(pattern, content, re.DOTALL)
if match:
    apps_content = match.group(1)
    # Find all app names
    app_pattern = r"['\"]([a-zA-Z_][a-zA-Z0-9_.]*)['\"]"
    apps = re.findall(app_pattern, apps_content)
    
    print("Found Django apps in INSTALLED_APPS:")
    for app in apps:
        print(f"  - {app}")
        
        # Check if it's a third-party Django app
        if app.startswith('django_'):
            # Convert to package name
            package = app.replace('_', '-')
            print(f"    → Potential package: {package}")
