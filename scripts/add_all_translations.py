#!/usr/bin/env python
"""
Complete translation script for all 5 languages
Adds translations for German, French, Spanish, and Polish
"""
import re
from pathlib import Path

# Base directory
base_dir = Path(r'd:\REPOS\fleet_mgmt_django')

# Comprehensive translations for all languages
translations = {
    # Navigation & Common
    "FleetManager": {
        "de": "FlottenManager",
        "fr": "GestionnaireDeFlotte",
        "es": "GestorDeFlota",
        "pl": "MenedżerFloty"
    },
    "Home Page": {
        "de": "Startseite",
        "fr": "Page d'accueil",
        "es": "Página de inicio",
        "pl": "Strona główna"
    },
    "Home - Car Fleet Management": {
        "de": "Startseite - Fahrzeugflottenmanagement",
        "fr": "Accueil - Gestion de flotte automobile",
        "es": "Inicio - Gestión de flotas de vehículos",
        "pl": "Strona główna - Zarządzanie flotą samochodową"
    },
    "Car Fleet Management": {
        "de": "Fahrzeugflottenmanagement",
        "fr": "Gestion de flotte automobile",
        "es": "Gestión de flotas de vehículos",
        "pl": "Zarządzanie flotą samochodową"
    },
    "Login": {
        "de": "Anmelden",
        "fr": "Connexion",
        "es": "Iniciar sesión",
        "pl": "Logowanie"
    },
    "Register": {
        "de": "Registrieren",
        "fr": "S'inscrire",
        "es": "Registrarse",
        "pl": "Rejestracja"
    },
    "Logout": {
        "de": "Abmelden",
        "fr": "Déconnexion",
        "es": "Cerrar sesión",
        "pl": "Wyloguj"
    },
    "Vehicles": {
        "de": "Fahrzeuge",
        "fr": "Véhicules",
        "es": "Vehículos",
        "pl": "Pojazdy"
    },
    "Maintenance": {
        "de": "Wartung",
        "fr": "Maintenance",
        "es": "Mantenimiento",
        "pl": "Konserwacja"
    },
    "Emergency": {
        "de": "Notfall",
        "fr": "Urgence",
        "es": "Emergencia",
        "pl": "Nagły wypadek"
    },
    "Admin": {
        "de": "Administrator",
        "fr": "Administrateur",
        "es": "Administrador",
        "pl": "Administrator"
    },
    
    # Home Page
    "Welcome to Fleet Management": {
        "de": "Willkommen beim Flottenmanagement",
        "fr": "Bienvenue dans la gestion de flotte",
        "es": "Bienvenido a la gestión de flotas",
        "pl": "Witamy w zarządzaniu flotą"
    },
    "Manage your vehicle fleet with ease and efficiency": {
        "de": "Verwalten Sie Ihre Fahrzeugflotte einfach und effizient",
        "fr": "Gérez votre flotte de véhicules avec facilité et efficacité",
        "es": "Gestione su flota de vehículos con facilidad y eficiencia",
        "pl": "Zarządzaj swoją flotą pojazdów z łatwością i wydajnością"
    },
    "System Overview": {
        "de": "Systemübersicht",
        "fr": "Aperçu du système",
        "es": "Resumen del sistema",
        "pl": "Przegląd systemu"
    },
    "System Online": {
        "de": "System Online",
        "fr": "Système en ligne",
        "es": "Sistema en línea",
        "pl": "System online"
    },
    "Quick Actions": {
        "de": "Schnellaktionen",
        "fr": "Actions rapides",
        "es": "Acciones rápidas",
        "pl": "Szybkie działania"
    },
    "Register new vehicle": {
        "de": "Neues Fahrzeug registrieren",
        "fr": "Enregistrer un nouveau véhicule",
        "es": "Registrar nuevo vehículo",
        "pl": "Zarejestruj nowy pojazd"
    },
    "Report incident": {
        "de": "Vorfall melden",
        "fr": "Signaler un incident",
        "es": "Reportar incidente",
        "pl": "Zgłoś incydent"
    },
    "Schedule service": {
        "de": "Service planen",
        "fr": "Planifier un service",
        "es": "Programar servicio",
        "pl": "Zaplanuj serwis"
    },
    "Recent Activity": {
        "de": "Letzte Aktivität",
        "fr": "Activité récente",
        "es": "Actividad reciente",
        "pl": "Ostatnia aktywność"
    },
    "System maintenance completed successfully": {
        "de": "Systemwartung erfolgreich abgeschlossen",
        "fr": "Maintenance du système terminée avec succès",
        "es": "Mantenimiento del sistema completado con éxito",
        "pl": "Konserwacja systemu zakończona pomyślnie"
    },
    "New fleet regulations update available": {
        "de": "Neue Flottenvorschriften-Aktualisierung verfügbar",
        "fr": "Nouvelle mise à jour des réglementations de flotte disponible",
        "es": "Nueva actualización de regulaciones de flota disponible",
        "pl": "Dostępna aktualizacja przepisów dotyczących floty"
    },
    "3 vehicles due for inspection this week": {
        "de": "3 Fahrzeuge müssen diese Woche inspiziert werden",
        "fr": "3 véhicules doivent être inspectés cette semaine",
        "es": "3 vehículos deben ser inspeccionados esta semana",
        "pl": "3 pojazdy wymagają przeglądu w tym tygodniu"
    },
    
    # Footer
    "Premium Fleet Management Solution": {
        "de": "Premium-Flottenmanagementsolution",
        "fr": "Solution de gestion de flotte premium",
        "es": "Solución premium de gestión de flotas",
        "pl": "Rozwiązanie premium do zarządzania flotą"
    },
    "Car Fleet Management System": {
        "de": "Fahrzeugflotten-Managementsystem",
        "fr": "Système de gestion de flotte automobile",
        "es": "Sistema de gestión de flota de vehículos",
        "pl": "System zarządzania flotą samochodową"
    },
    "Toggle Theme": {
        "de": "Design wechseln",
        "fr": "Changer le thème",
        "es": "Cambiar tema",
        "pl": "Przełącz motyw"
    },
    "Change Language": {
        "de": "Sprache ändern",
        "fr": "Changer de langue",
        "es": "Cambiar idioma",
        "pl": "Zmień język"
    },
    
    # Login / Register
    "Login - Car Fleet Management": {
        "de": "Anmelden - Fahrzeugflottenmanagement",
        "fr": "Connexion - Gestion de flotte automobile",
        "es": "Iniciar sesión - Gestión de flotas",
        "pl": "Logowanie - Zarządzanie flotą"
    },
    "Welcome Back": {
        "de": "Willkommen zurück",
        "fr": "Bon retour",
        "es": "Bienvenido de nuevo",
        "pl": "Witamy ponownie"
    },
    "Sign in to access your fleet dashboard": {
        "de": "Melden Sie sich an, um auf Ihr Flotten-Dashboard zuzugreifen",
        "fr": "Connectez-vous pour accéder à votre tableau de bord",
        "es": "Inicie sesión para acceder a su panel de flota",
        "pl": "Zaloguj się, aby uzyskać dostęp do pulpitu floty"
    },
    "Username": {
        "de": "Benutzername",
        "fr": "Nom d'utilisateur",
        "es": "Nombre de usuario",
        "pl": "Nazwa użytkownika"
    },
    "Password": {
        "de": "Passwort",
        "fr": "Mot de passe",
        "es": "Contraseña",
        "pl": "Hasło"
    },
    "Sign In": {
        "de": "Anmelden",
        "fr": "Se connecter",
        "es": "Ingresar",
        "pl": "Zaloguj się"
    },
    "Don't have an account?": {
        "de": "Haben Sie noch kein Konto?",
        "fr": "Vous n'avez pas de compte ?",
        "es": "¿No tienes una cuenta?",
        "pl": "Nie masz konta?"
    },
    "Register here": {
        "de": "Hier registrieren",
        "fr": "Inscrivez-vous ici",
        "es": "Regístrate aquí",
        "pl": "Zarejestruj się tutaj"
    },
    "Register - Car Fleet Management": {
        "de": "Registrieren - Fahrzeugflottenmanagement",
        "fr": "S'inscrire - Gestion de flotte automobile",
        "es": "Registrarse - Gestión de flotas",
        "pl": "Rejestracja - Zarządzanie flotą"
    },
    "Create Account": {
        "de": "Konto erstellen",
        "fr": "Créer un compte",
        "es": "Crear cuenta",
        "pl": "Utwórz konto"
    },
    "Join the fleet management platform": {
        "de": "Treten Sie der Flottenmanagement-Plattform bei",
        "fr": "Rejoignez la plateforme de gestion de flotte",
        "es": "Únete a la plataforma de gestión de flotas",
        "pl": "Dołącz do platformy zarządzania flotą"
    },
    "Already have an account?": {
        "de": "Haben Sie bereits ein Konto?",
        "fr": "Vous avez déjà un compte ?",
        "es": "¿Ya tienes una cuenta?",
        "pl": "Masz już konto?"
    },
    "Login here": {
        "de": "Hier anmelden",
        "fr": "Connectez-vous ici",
        "es": "Inicia sesión aquí",
        "pl": "Zaloguj się tutaj"
    },

    # Emergency List
    "Emergency Incidents": {
        "de": "Notfälle",
        "fr": "Incidents d'urgence",
        "es": "Incidentes de emergencia",
        "pl": "Incydenty awaryjne"
    },
    "Report New Incident": {
        "de": "Neuen Vorfall melden",
        "fr": "Signaler un nouvel incident",
        "es": "Reportar nuevo incidente",
        "pl": "Zgłoś nowy incydent"
    },
    "Location": {
        "de": "Standort",
        "fr": "Emplacement",
        "es": "Ubicación",
        "pl": "Lokalizacja"
    },
    "No emergency incidents found.": {
        "de": "Keine Notfälle gefunden.",
        "fr": "Aucun incident d'urgence trouvé.",
        "es": "No se encontraron incidentes de emergencia.",
        "pl": "Nie znaleziono incydentów awaryjnych."
    },
    
    # Model Choices & Verbose Names
    "Truck": {"de": "LKW", "fr": "Camion", "es": "Camión", "pl": "Ciężarówka"},
    "Van": {"de": "Transporter", "fr": "Fourgonnette", "es": "Furgoneta", "pl": "Furgonetka"},
    "SUV": {"de": "SUV", "fr": "SUV", "es": "SUV", "pl": "SUV"},
    "Pickup": {"de": "Pickup", "fr": "Pickup", "es": "Camioneta", "pl": "Pickup"},
    
    "Diesel": {"de": "Diesel", "fr": "Diesel", "es": "Diésel", "pl": "Diesel"},
    "Petrol": {"de": "Benzin", "fr": "Essence", "es": "Gasolina", "pl": "Benzyna"},
    "Hybrid": {"de": "Hybrid", "fr": "Hybride", "es": "Híbrido", "pl": "Hybryda"},
    "Electric": {"de": "Elektrisch", "fr": "Électrique", "es": "Eléctrico", "pl": "Elektryczny"},
    
    "Manual": {"de": "Manuell", "fr": "Manuel", "es": "Manual", "pl": "Manualna"},
    "Automatic": {"de": "Automatik", "fr": "Automatique", "es": "Automático", "pl": "Automatyczna"},
    
    "Available": {"de": "Verfügbar", "fr": "Disponible", "es": "Disponible", "pl": "Dostępny"},
    "In Use": {"de": "In Benutzung", "fr": "En cours d'utilisation", "es": "En uso", "pl": "W użyciu"},
    "In Maintenance": {"de": "In Wartung", "fr": "En maintenance", "es": "En mantenimiento", "pl": "W konserwacji"},
    "Out of Service": {"de": "Außer Betrieb", "fr": "Hors service", "es": "Fuera de servicio", "pl": "Wyłączony z eksploatacji"},
    
    "Routine Maintenance": {"de": "Routinewartung", "fr": "Maintenance de routine", "es": "Mantenimiento de rutina", "pl": "Rutynowa konserwacja"},
    "Repair": {"de": "Reparatur", "fr": "Réparation", "es": "Reparación", "pl": "Naprawa"},
    "Inspection": {"de": "Inspektion", "fr": "Inspection", "es": "Inspección", "pl": "Przegląd"},
    
    "Scheduled": {"de": "Geplant", "fr": "Planifié", "es": "Programado", "pl": "Zaplanowany"},
    "In Progress": {"de": "In Bearbeitung", "fr": "En cours", "es": "En progreso", "pl": "W toku"},
    "Completed": {"de": "Abgeschlossen", "fr": "Terminé", "es": "Completado", "pl": "Zakończony"},
    "Cancelled": {"de": "Abgebrochen", "fr": "Annulé", "es": "Cancelado", "pl": "Anulowany"},
    
    "Accident": {"de": "Unfall", "fr": "Accident", "es": "Accidente", "pl": "Wypadek"},
    "Breakdown": {"de": "Panne", "fr": "Panne", "es": "Avería", "pl": "Awaria"},
    "Medical Emergency": {"de": "Medizinischer Notfall", "fr": "Urgence médicale", "es": "Emergencia médica", "pl": "Nagły wypadek medyczny"},
    "Theft": {"de": "Diebstahl", "fr": "Vol", "es": "Robo", "pl": "Kradzież"},
    
    "Reported": {"de": "Gemeldet", "fr": "Signalé", "es": "Reportado", "pl": "Zgłoszony"},
    "Responding": {"de": "Reagierend", "fr": "En intervention", "es": "Respondiendo", "pl": "Reagujący"},
    "Resolved": {"de": "Gelöst", "fr": "Résolu", "es": "Resuelto", "pl": "Rozwiązany"},
    "Closed": {"de": "Geschlossen", "fr": "Fermé", "es": "Cerrado", "pl": "Zamknięty"},
    
    "Maintenance Records": {"de": "Wartungsprotokolle", "fr": "Dossiers de maintenance", "es": "Registros de mantenimiento", "pl": "Rejestry konserwacji"},
    "Add New Maintenance Record": {"de": "Neuen Wartungseintrag hinzufügen", "fr": "Ajouter un dossier de maintenance", "es": "Agregar nuevo registro", "pl": "Dodaj nowy wpis konserwacji"},
    "Add New Vehicle": {"de": "Neues Fahrzeug hinzufügen", "fr": "Ajouter un nouveau véhicule", "es": "Agregar nuevo vehículo", "pl": "Dodaj nowy pojazd"},
    "Vehicle List": {"de": "Fahrzeugliste", "fr": "Liste des véhicules", "es": "Lista de vehículos", "pl": "Lista pojazdów"},
    "Vehicle": {"de": "Fahrzeug", "fr": "Véhicule", "es": "Vehículo", "pl": "Pojazd"},
    "Actions": {"de": "Aktionen", "fr": "Actions", "es": "Acciones", "pl": "Akcje"},
    "Type": {"de": "Typ", "fr": "Type", "es": "Tipo", "pl": "Typ"},
    "Description": {"de": "Beschreibung", "fr": "Description", "es": "Descripción", "pl": "Opis"},
    "Scheduled Date": {"de": "Geplantes Datum", "fr": "Date prévue", "es": "Fecha programada", "pl": "Zaplanowana data"},
}

def add_translations_to_po(lang_code):
    """Add translations to a specific language .po file"""
    po_file = base_dir / f"locale/{lang_code}/LC_MESSAGES/django.po"
    
    if not po_file.exists():
        print(f"❌ {lang_code}: .po file not found")
        return
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    added_count = 0
    updated_count = 0
    
    for english, trans_dict in translations.items():
        if lang_code not in trans_dict:
            continue
            
        translation = trans_dict[lang_code]
        
        # Check if active msgid exists using regex to avoid matching commented out lines
        # We look for msgid "..." at the start of a line
        active_pattern = re.compile(f'^msgid "{re.escape(english)}"', re.MULTILINE)
        
        if active_pattern.search(content):
            # Check if it has empty translation
            # We look for msgid "..." followed immediately by msgstr ""
            empty_pattern = re.compile(f'^msgid "{re.escape(english)}"\nmsgstr ""', re.MULTILINE)
            if empty_pattern.search(content):
                # Add translation
                replacement = f'msgid "{english}"\nmsgstr "{translation}"'
                content = empty_pattern.sub(replacement, content)
                updated_count += 1
        else:
            # Add new entry at the end
            new_entry = f'\nmsgid "{english}"\nmsgstr "{translation}"\n'
            content = content.rstrip() + new_entry + '\n'
            added_count += 1
    
    # Write back
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {lang_code.upper()}: {updated_count} updated, {added_count} added")

# Process all languages
print("Adding translations for all languages...")
print("="*50)

for lang in ['de', 'fr', 'es', 'pl']:
    add_translations_to_po(lang)

print("="*50)
print("\n✅ All translations added!")
print("\nNext: Run 'python manage.py compilemessages' to compile")
