"""
WSGI config for mysite project.
Updated for Vercel Deployment.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
app = application  # <--- THIS LINE IS MANDATORY FOR VERCEL