from django.test import Client
from django.urls import reverse
import pytest
from CarFleetManagement.vehicles.models import Vehicle
from CarFleetManagement.accounts.models import CustomUser
from datetime import date
import uuid

@pytest.mark.django_db
def test_vehicle_create_form_post_creates_vehicle():
    # Create a manager user (or admin) to pass the permission checks
    user, created = CustomUser.objects.get_or_create(username='test_manager', defaults={'email': 'm@example.com'})
    if created:
        user.set_password('pass')
        user.is_staff = True
        user.save()

    client = Client()
    logged = client.login(username='test_manager', password='pass')
    if not logged:
        # try force login if login via credentials failed
        client.force_login(user)

    url = reverse('vehicles:vehicle_create')
    get_resp = client.get(url)
    assert get_resp.status_code in (200, 302)

    # Post minimal valid data (fields from VehicleCreateView.fields)
    suffix = uuid.uuid4().hex[:8].upper()
    payload = {
        'brand': 'TestBrand',
        'model': 'T1',
        'year': 2020,
        'license_plate': f'TEST-{suffix}',
        # VIN must be <=17 chars; create a unique-ish value
        'vin': f'VIN{uuid.uuid4().hex[:13].upper()}',
        'color': 'Blue',
        # Use raw choice values defined on Vehicle model
        'fuel_type': 'PETROL',
        'transmission': 'MANUAL',
        'vehicle_type': 'SUV',
        'mileage': 10000,
        'last_service_date': date.today().isoformat(),
        'next_service_date': date.today().isoformat(),
        'insurance_expiry': date.today().isoformat(),
        'status': 'AVAILABLE',
    }

    post_resp = client.post(url, data=payload, follow=True)
    # expect redirect to list or detail
    assert post_resp.status_code in (200, 302), f"Unexpected status {post_resp.status_code} - content: {post_resp.content[:1000]!r}"

    # Check DB: vehicle with license_plate created
    lp = payload['license_plate']
    exists = Vehicle.objects.filter(license_plate=lp).exists()
    assert exists, (
        "Vehicle not created. Server response (truncated): "
        f"status={post_resp.status_code}; content={post_resp.content.decode('utf-8')[:4000]}"
    )
    v = Vehicle.objects.get(license_plate=lp)
    assert v.brand == payload['brand']
    assert v.vin == payload['vin']
