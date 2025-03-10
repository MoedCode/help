import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "help_backend.settings")

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    import sys

    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])
