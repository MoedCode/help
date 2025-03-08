from django.core.management import execute_from_command_line
import sys

if __name__ == '__main__':
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)
