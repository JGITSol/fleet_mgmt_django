#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        class DjangoImportError(ImportError):
            def __init__(self):
                super().__init__("Django import failure")

        raise DjangoImportError() from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
