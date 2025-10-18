"""
ASGI config for voiceai project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

my_project/asgi.py: Similar to wsgi.py, asgi.py is the entry point for asynchronous web servers. It stands for Asynchronous Server Gateway Interface and facilitates the handling of asynchronous HTTP requests.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voiceai.settings')

application = get_asgi_application()
