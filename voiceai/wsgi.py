"""
WSGI config for voiceai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/

my_project/wsgi.py: Short for Web Server Gateway Interface, wsgi.py serves as the entry point for your application when deployed on a production server. It's the bridge connecting your application to the web server, enabling it to handle incoming requests.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voiceai.settings')

application = get_wsgi_application()
