@echo off
echo Running individual test files...

cd %~dp0
set DJANGO_SETTINGS_MODULE=CarFleetManagement.settings

echo Testing accounts...
python -m pytest tests\test_accounts.py -v

echo Testing API...
python -m pytest tests\test_api.py -v

echo Testing emergency...
python -m pytest tests\test_emergency.py -v

echo Testing maintenance...
python -m pytest tests\test_maintenance.py -v

echo Testing vehicles...
python -m pytest tests\test_vehicles.py -v

echo All tests completed!
