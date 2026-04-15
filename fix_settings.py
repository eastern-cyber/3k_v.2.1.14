
import re

with open('_core/settings.py', 'r') as f:
    content = f.read()

# Remove django_browser_reload from INSTALLED_APPS
content = re.sub(r"'django_browser_reload',\s*", "", content)
content = re.sub(r'"django_browser_reload",\s*', "", content)

# Also check for it in other places
content = re.sub(r"#.*django_browser_reload.*\n", "", content)

with open('_core/settings.py', 'w') as f:
    f.write(content)

print("Removed django_browser_reload from settings.py")
