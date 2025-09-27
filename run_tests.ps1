# PowerShell helper to run tests inside venv
if (Test-Path .\venv\Scripts\Activate.ps1) {
    .\venv\Scripts\Activate.ps1
}
pytest -q
