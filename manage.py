#!/usr/bin/env python
# the classic django manage.py

import os
import sys

def main():
    # this is where all the django magic starts
    # if this breaks, nothing works lol 💀
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # if django isn't installed, we're toast
        # probably forgot to activate the venv again 🤦‍♂️
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

