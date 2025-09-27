from django.core.management.base import BaseCommand
from vehicles.models import Vehicle


class Command(BaseCommand):
    help = 'Remove all demo vehicles from the database.'

    def handle(self, *args, **options):
        deleted, _ = Vehicle.objects.filter(license_plate__startswith='DEMO-').delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {deleted} demo vehicles.'))
