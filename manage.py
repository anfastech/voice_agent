#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
manage.py: This small but mighty script serves as the gateway to various Django management commands. 
It's the tool through which you initiate the development server, create applications, run migrations, and more. `manage.py` is the conductor's baton, guiding your project's activities.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voiceai.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
