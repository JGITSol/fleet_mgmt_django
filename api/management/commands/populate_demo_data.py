from django.core.management.base import BaseCommand
from vehicles.models import Vehicle


class Command(BaseCommand):
    help = 'Populate the database with demo vehicles for testing and demos.'

    def handle(self, *args, **options):
        demo_vehicles = [
            {'name': 'Demo Car 1', 'license_plate': 'DEMO-001'},
            {'name': 'Demo Car 2', 'license_plate': 'DEMO-002'},
            {'name': 'Demo Car 3', 'license_plate': 'DEMO-003'},
        ]
        for vehicle in demo_vehicles:
            Vehicle.objects.get_or_create(name=vehicle['name'], license_plate=vehicle['license_plate'])
        self.stdout.write(self.style.SUCCESS('Demo vehicles added.'))
