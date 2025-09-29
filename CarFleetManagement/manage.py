#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Add the parent directory to Python path so CarFleetManagement module can be found
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")
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
