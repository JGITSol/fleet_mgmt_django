Car Fleet Manager — repozytorium

Cel: szybkie uruchomienie projektu Django z REST API (MVP). Ten README ma szybkie instrukcje uruchomienia deweloperskiego, testów i dockera.

Szybki start (lokalnie)

1. Skopiuj przykładowy plik zmiennych środowiskowych:

   cp .env.example .env
   # Windows PowerShell:
   # Copy-Item .env.example .env

2. (opcjonalnie) Stwórz virtualenv i aktywuj:

   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Zainstaluj zależności:

   pip install -r requirements.txt

4. Uruchom migracje i stwórz superusera:

   python manage.py migrate
   python manage.py createsuperuser

5. Uruchom serwer deweloperski:

   python manage.py runserver

Uruchamianie testów

W PowerShell uruchom:

   .\run_tests.ps1

Lub bez skryptu:

   .\venv\Scripts\Activate.ps1; pytest -q

Docker

Uruchomienie przez docker-compose (wymaga Docker):

   docker-compose up --build

Co dodałem (szybkie zmiany infra)

- `.env.example` — przykładowy plik środowiskowy
- `.github/workflows/ci.yml` — podstawowy CI uruchamiający testy
- `run_tests.ps1` — prosty skrypt uruchamiający testy w PowerShell

Następne kroki (zalecane)

1. Naprawić redirecty z widoków do /accounts/login/ i zapewnić, że API zwraca poprawne kody (401/403) dla żądań nieautoryzowanych — obecnie wiele testów oczekuje JWT/401, a zachowanie to redirect 302.
2. Ujednolicić autentykację: użyć wyłącznie JWT dla API (REST endpoints) i Session/Auth mixinów tylko dla HTML views.
3. Dodać `.env` do `.gitignore` i dokumentację dla zmiennych produkcyjnych (sekrety, DB).
4. Dodać prosty skrypt do budowy obrazu produkcyjnego i wskazówki deploy.

Jeżeli chcesz, mogę teraz:
- spróbować naprawić testy związane z redirectami (najpierw przeanalizować middleware i dekoratory używane w `CarFleetManagement/api/urls.py` i endpointach),
- poprawić testy wymagające API-keys przez mockowanie lub bezpieczne domyślne wartości,
- ujednolicić konfigurację REST_FRAMEWORK i LOGIN_URL tak, by API odpowiadało JSON 401 zamiast redirect.
