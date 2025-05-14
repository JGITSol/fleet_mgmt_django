from django.core.management.base import BaseCommand
from api.models import Vehicle  # Example, adjust as needed

class Command(BaseCommand):
    help = 'Populate the database with demo vehicles for testing and demos.'

    def handle(self, *args, **options):
        demo_vehicles = [
            {'name': 'Demo Car 1', 'license_plate': 'DEMO-001'},
            {'name': 'Demo Car 2', 'license_plate': 'DEMO-002'},
            {'name': 'Demo Car 3', 'license_plate': 'DEMO-003'},
        ]
        created_count = 0
        for data in demo_vehicles:
            obj, created = Vehicle.objects.get_or_create(**data)
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Populated {created_count} demo vehicles.'))
