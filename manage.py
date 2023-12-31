#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pathlib
import dotenv


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    env_path = pathlib.Path() / '.env'
    if env_path.exists():
        dotenv.load_dotenv(env_path)
    if os.environ:
        print(os.environ)
    else:
        print('no variables')
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
