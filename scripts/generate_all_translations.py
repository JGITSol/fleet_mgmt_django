"""
Comprehensive translation generator for Django Fleet Management System
Generates translations for all strings found in .po files for 5 languages:
- English (en) - base language
- Polish (pl)
- French (fr)
- Spanish (es)
- German (de)
"""

import os
import re
from pathlib import Path

# Translation dictionaries
TRANSLATIONS = {
    # Navigation & Common UI
    "Home": {"pl": "Strona główna", "fr": "Accueil", "es": "Inicio", "de": "Startseite"},
    "FleetManager": {"pl": "Menedżer Floty", "fr": "Gestionnaire de Flotte", "es": "Gestor de Flota", "de": "Flottenmanager"},
    "Vehicles": {"pl": "Pojazdy", "fr": "Véhicules", "es": "Vehículos", "de": "Fahrzeuge"},
    "Maintenance": {"pl": "Konserwacja", "fr": "Maintenance", "es": "Mantenimiento", "de": "Wartung"},
    "Emergency": {"pl": "Nagłe wypadki", "fr": "Urgence", "es": "Emergencia", "de": "Notfall"},
    "Admin": {"pl": "Administrator", "fr": "Admin", "es": "Admin", "de": "Admin"},
    "Login": {"pl": "Zaloguj się", "fr": "Connexion", "es": "Iniciar sesión", "de": "Anmelden"},
    "Logout": {"pl": "Wyloguj się", "fr": "Déconnexion", "es": "Cerrar sesión", "de": "Abmelden"},
    "Register": {"pl": "Zarejestruj się", "fr": "S'inscrire", "es": "Registrarse", "de": "Registrieren"},
    "Toggle Theme": {"pl": "Przełącz motyw", "fr": "Changer de thème", "es": "Cambiar tema", "de": "Design wechseln"},
    
    # Home page
    "Welcome to Fleet Management": {"pl": "Witamy w Zarządzaniu Flotą", "fr": "Bienvenue dans la Gestion de Flotte", "es": "Bienvenido a la Gestión de Flota", "de": "Willkommen beim Flottenmanagement"},
    "Manage your vehicle fleet with ease and efficiency": {"pl": "Zarządzaj swoją flotą pojazdów z łatwością i wydajnością", "fr": "Gérez votre flotte de véhicules avec facilité et efficacité", "es": "Gestione su flota de vehículos con facilidad y eficiencia", "de": "Verwalten Sie Ihre Fahrzeugflotte einfach und effizient"},
    "System Overview": {"pl": "Przegląd systemu", "fr": "Aperçu du système", "es": "Resumen del sistema", "de": "Systemübersicht"},
    "System Online": {"pl": "System online", "fr": "Système en ligne", "es": "Sistema en línea", "de": "System online"},
    "Quick Actions": {"pl": "Szybkie działania", "fr": "Actions rapides", "es": "Acciones rápidas", "de": "Schnellaktionen"},
    "Recent Activity": {"pl": "Ostatnia aktywność", "fr": "Activité récente", "es": "Actividad reciente", "de": "Letzte Aktivität"},
    "Register new vehicle": {"pl": "Zarejestruj nowy pojazd", "fr": "Enregistrer un nouveau véhicule", "es": "Registrar nuevo vehículo", "de": "Neues Fahrzeug registrieren"},
    "Report incident": {"pl": "Zgłoś incydent", "fr": "Signaler un incident", "es": "Reportar incidente", "de": "Vorfall melden"},
    "Schedule service": {"pl": "Zaplanuj serwis", "fr": "Planifier un service", "es": "Programar servicio", "de": "Service planen"},
    "System maintenance completed successfully": {"pl": "Konserwacja systemu zakończona pomyślnie", "fr": "Maintenance du système terminée avec succès", "es": "Mantenimiento del sistema completado con éxito", "de": "Systemwartung erfolgreich abgeschlossen"},
    "New fleet regulations update available": {"pl": "Dostępna nowa aktualizacja przepisów flotowych", "fr": "Nouvelle mise à jour des règlements de flotte disponible", "es": "Nueva actualización de regulaciones de flota disponible", "de": "Neue Flottenvorschriften-Aktualisierung verfügbar"},
    "3 vehicles due for inspection this week": {"pl": "3 pojazdy wymagają przeglądu w tym tygodniu", "fr": "3 véhicules à inspecter cette semaine", "es": "3 vehículos pendientes de inspección esta semana", "de": "3 Fahrzeuge müssen diese Woche inspiziert werden"},
    
    # Footer
    "Premium Fleet Management Solution": {"pl": "Rozwiązanie Premium do Zarządzania Flotą", "fr": "Solution Premium de Gestion de Flotte", "es": "Solución Premium de Gestión de Flota", "de": "Premium-Flottenmanagementsolution"},
    "Car Fleet Management System": {"pl": "System Zarządzania Flotą Samochodową", "fr": "Système de Gestion de Flotte Automobile", "es": "Sistema de Gestión de Flota de Vehículos", "de": "Fahrzeugflottenmanagementsystem"},
    "Car Fleet Management": {"pl": "Zarządzanie Flotą Samochodową", "fr": "Gestion de Flotte Automobile", "es": "Gestión de Flota de Vehículos", "de": "Fahrzeugflottenmanagement"},
    
    # Login/Register
    "Username": {"pl": "Nazwa użytkownika", "fr": "Nom d'utilisateur", "es": "Nombre de usuario", "de": "Benutzername"},
    "Password": {"pl": "Hasło", "fr": "Mot de passe", "es": "Contraseña", "de": "Passwort"},
    "Email": {"pl": "E-mail", "fr": "E-mail", "es": "Correo electrónico", "de": "E-Mail"},
    "First Name": {"pl": "Imię", "fr": "Prénom", "es": "Nombre", "de": "Vorname"},
    "Last Name": {"pl": "Nazwisko", "fr": "Nom", "es": "Apellido", "de": "Nachname"},
    "Sign In": {"pl": "Zaloguj się", "fr": "Se connecter", "es": "Iniciar sesión", "de": "Anmelden"},
    "Sign Up": {"pl": "Zarejestruj się", "fr": "S'inscrire", "es": "Registrarse", "de": "Registrieren"},
    "Forgot Password?": {"pl": "Zapomniałeś hasła?", "fr": "Mot de passe oublié?", "es": "¿Olvidó su contraseña?", "de": "Passwort vergessen?"},
    "Remember me": {"pl": "Zapamiętaj mnie", "fr": "Se souvenir de moi", "es": "Recuérdame", "de": "Angemeldet bleiben"},
    
    # Common actions
    "Create": {"pl": "Utwórz", "fr": "Créer", "es": "Crear", "de": "Erstellen"},
    "Edit": {"pl": "Edytuj", "fr": "Modifier", "es": "Editar", "de": "Bearbeiten"},
    "Delete": {"pl": "Usuń", "fr": "Supprimer", "es": "Eliminar", "de": "Löschen"},
    "Save": {"pl": "Zapisz", "fr": "Enregistrer", "es": "Guardar", "de": "Speichern"},
    "Cancel": {"pl": "Anuluj", "fr": "Annuler", "es": "Cancelar", "de": "Abbrechen"},
    "Submit": {"pl": "Prześlij", "fr": "Soumettre", "es": "Enviar", "de": "Absenden"},
    "Search": {"pl": "Szukaj", "fr": "Rechercher", "es": "Buscar", "de": "Suchen"},
    "Filter": {"pl": "Filtruj", "fr": "Filtrer", "es": "Filtrar", "de": "Filtern"},
    "View": {"pl": "Zobacz", "fr": "Voir", "es": "Ver", "de": "Ansehen"},
    "Details": {"pl": "Szczegóły", "fr": "Détails", "es": "Detalles", "de": "Details"},
    "Back": {"pl": "Wstecz", "fr": "Retour", "es": "Volver", "de": "Zurück"},
    "Next": {"pl": "Dalej", "fr": "Suivant", "es": "Siguiente", "de": "Weiter"},
    "Previous": {"pl": "Poprzedni", "fr": "Précédent", "es": "Anterior", "de": "Vorherige"},
    
    # Vehicle related
    "Vehicle List": {"pl": "Lista pojazdów", "fr": "Liste des véhicules", "es": "Lista de vehículos", "de": "Fahrzeugliste"},
    "Add Vehicle": {"pl": "Dodaj pojazd", "fr": "Ajouter un véhicule", "es": "Agregar vehículo", "de": "Fahrzeug hinzufügen"},
    "Vehicle Details": {"pl": "Szczegóły pojazdu", "fr": "Détails du véhicule", "es": "Detalles del vehículo", "de": "Fahrzeugdetails"},
    "License Plate": {"pl": "Tablica rejestracyjna", "fr": "Plaque d'immatriculation", "es": "Matrícula", "de": "Kennzeichen"},
    "Make": {"pl": "Marka", "fr": "Marque", "es": "Marca", "de": "Marke"},
    "Model": {"pl": "Model", "fr": "Modèle", "es": "Modelo", "de": "Modell"},
    "Year": {"pl": "Rok", "fr": "Année", "es": "Año", "de": "Jahr"},
    "VIN": {"pl": "VIN", "fr": "VIN", "es": "VIN", "de": "FIN"},
    "Status": {"pl": "Status", "fr": "Statut", "es": "Estado", "de": "Status"},
    "Mileage": {"pl": "Przebieg", "fr": "Kilométrage", "es": "Kilometraje", "de": "Kilometerstand"},
    
    # Maintenance related
    "Maintenance List": {"pl": "Lista konserwacji", "fr": "Liste de maintenance", "es": "Lista de mantenimiento", "de": "Wartungsliste"},
    "Schedule Maintenance": {"pl": "Zaplanuj konserwację", "fr": "Planifier la maintenance", "es": "Programar mantenimiento", "de": "Wartung planen"},
    "Maintenance Type": {"pl": "Typ konserwacji", "fr": "Type de maintenance", "es": "Tipo de mantenimiento", "de": "Wartungstyp"},
    "Service Date": {"pl": "Data serwisu", "fr": "Date de service", "es": "Fecha de servicio", "de": "Servicedatum"},
    "Cost": {"pl": "Koszt", "fr": "Coût", "es": "Costo", "de": "Kosten"},
    "Notes": {"pl": "Notatki", "fr": "Notes", "es": "Notas", "de": "Notizen"},
    
    # Emergency related
    "Emergency List": {"pl": "Lista nagłych wypadków", "fr": "Liste des urgences", "es": "Lista de emergencias", "de": "Notfallliste"},
    "Report Emergency": {"pl": "Zgłoś nagły wypadek", "fr": "Signaler une urgence", "es": "Reportar emergencia", "de": "Notfall melden"},
    "Incident Type": {"pl": "Typ incydentu", "fr": "Type d'incident", "es": "Tipo de incidente", "de": "Vorfalltyp"},
    "Location": {"pl": "Lokalizacja", "fr": "Emplacement", "es": "Ubicación", "de": "Standort"},
    "Description": {"pl": "Opis", "fr": "Description", "es": "Descripción", "de": "Beschreibung"},
    "Severity": {"pl": "Dotkliwość", "fr": "Gravité", "es": "Severidad", "de": "Schweregrad"},
    "Resolved": {"pl": "Rozwiązany", "fr": "Résolu", "es": "Resuelto", "de": "Gelöst"},
    "Pending": {"pl": "Oczekujący", "fr": "En attente", "es": "Pendiente", "de": "Ausstehend"},
}

def update_po_file(po_file_path, language_code):
    """Update a .po file with translations"""
    if not os.path.exists(po_file_path):
        print(f"⚠️  File not found: {po_file_path}")
        return
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_count = 0
    
    # Find all msgid/msgstr pairs
    pattern = r'msgid "([^"]+)"\nmsgstr ""'
    
    def replace_translation(match):
        nonlocal updated_count
        msgid = match.group(1)
        
        if msgid in TRANSLATIONS and language_code in TRANSLATIONS[msgid]:
            updated_count += 1
            translation = TRANSLATIONS[msgid][language_code]
            return f'msgid "{msgid}"\nmsgstr "{translation}"'
        return match.group(0)
    
    content = re.sub(pattern, replace_translation, content)
    
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {updated_count} translations in {language_code}.po")

def main():
    base_dir = Path('locale')
    
    languages = {
        'pl': 'Polish',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German'
    }
    
    print("=" * 60)
    print("Generating Comprehensive Translations")
    print("=" * 60)
    
    for lang_code, lang_name in languages.items():
        print(f"\n📝 Processing {lang_name} ({lang_code})...")
        po_file = base_dir / lang_code / 'LC_MESSAGES' / 'django.po'
        update_po_file(str(po_file), lang_code)
    
    print("\n" + "=" * 60)
    print(f"✅ Translation generation complete!")
    print(f"📊 Total strings translated: {len(TRANSLATIONS)}")
    print(f"🌍 Languages: {', '.join(languages.values())}")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python manage.py compilemessages")
    print("2. Restart the Django server")
    print("3. Test each language version")

if __name__ == '__main__':
    main()
