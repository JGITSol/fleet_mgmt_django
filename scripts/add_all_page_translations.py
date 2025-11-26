#!/usr/bin/env python
"""
Complete translation script for ALL remaining pages
Adds comprehensive translations for vehicles, maintenance, emergency pages
"""
from pathlib import Path
import re

# Comprehensive translations for all remaining pages
all_translations = {
    # Vehicle pages
    "Vehicles": {"de": "Fahrzeuge", "fr": "Véhicules", "es": "Vehículos", "pl": "Pojazdy"},
    "Vehicle List": {"de": "Fahrzeugliste", "fr": "Liste des véhicules", "es": "Lista de vehículos", "pl": "Lista pojazdów"},
    "Add Vehicle": {"de": "Fahrzeug hinzufügen", "fr": "Ajouter un véhicule", "es": "Agregar vehículo", "pl": "Dodaj pojazd"},
    "Edit Vehicle": {"de": "Fahrzeug bearbeiten", "fr": "Modifier le véhicule", "es": "Editar vehículo", "pl": "Edytuj pojazd"},
    "Delete Vehicle": {"de": "Fahrzeug löschen", "fr": "Supprimer le véhicule", "es": "Eliminar vehículo", "pl": "Usuń pojazd"},
    "Vehicle Details": {"de": "Fahrzeugdetails", "fr": "Détails du véhicule", "es": "Detalles del vehículo", "pl": "Szczegóły pojazdu"},
    "Make": {"de": "Marke", "fr": "Marque", "es": "Marca", "pl": "Marka"},
    "Model": {"de": "Modell", "fr": "Modèle", "es": "Modelo", "pl": "Model"},
    "Year": {"de": "Jahr", "fr": "Année", "es": "Año", "pl": "Rok"},
    "License Plate": {"de": "Kennzeichen", "fr": "Plaque d'immatriculation", "es": "Matrícula", "pl": "Tablica rejestracyjna"},
    "VIN": {"de": "Fahrgestellnummer", "fr": "NIV", "es": "VIN", "pl": "VIN"},
    "Status": {"de": "Status", "fr": "Statut", "es": "Estado", "pl": "Status"},
    "Mileage": {"de": "Kilometerstand", "fr": "Kilométrage", "es": "Kilometraje", "pl": "Przebieg"},
    
    # Maintenance pages
    "Maintenance": {"de": "Wartung", "fr": "Maintenance", "es": "Mantenimiento", "pl": "Konserwacja"},
    "Maintenance List": {"de": "Wartungsliste", "fr": "Liste de maintenance", "es": "Lista de mantenimiento", "pl": "Lista konserwacji"},
    "Add Maintenance": {"de": "Wartung hinzufügen", "fr": "Ajouter une maintenance", "es": "Agregar mantenimiento", "pl": "Dodaj konserwację"},
    "Edit Maintenance": {"de": "Wartung bearbeiten", "fr": "Modifier la maintenance", "es": "Editar mantenimiento", "pl": "Edytuj konserwację"},
    "Delete Maintenance": {"de": "Wartung löschen", "fr": "Supprimer la maintenance", "es": "Eliminar mantenimiento", "pl": "Usuń konserwację"},
    "Maintenance Details": {"de": "Wartungsdetails", "fr": "Détails de maintenance", "es": "Detalles de mantenimiento", "pl": "Szczegóły konserwacji"},
    "Service Type": {"de": "Servicetyp", "fr": "Type de service", "es": "Tipo de servicio", "pl": "Typ serwisu"},
    "Date": {"de": "Datum", "fr": "Date", "es": "Fecha", "pl": "Data"},
    "Cost": {"de": "Kosten", "fr": "Coût", "es": "Costo", "pl": "Koszt"},
    "Description": {"de": "Beschreibung", "fr": "Description", "es": "Descripción", "pl": "Opis"},
    "Technician": {"de": "Techniker", "fr": "Technicien", "es": "Técnico", "pl": "Technik"},
    
    # Emergency pages
    "Emergency": {"de": "Notfall", "fr": "Urgence", "es": "Emergencia", "pl": "Nagły wypadek"},
    "Emergency List": {"de": "Notfallliste", "fr": "Liste d'urgence", "es": "Lista de emergencias", "pl": "Lista nagłych wypadków"},
    "Report Emergency": {"de": "Notfall melden", "fr": "Signaler une urgence", "es": "Reportar emergencia", "pl": "Zgłoś nagły wypadek"},
    "Emergency Details": {"de": "Notfalldetails", "fr": "Détails d'urgence", "es": "Detalles de emergencia", "pl": "Szczegóły nagłego wypadku"},
    "Incident Type": {"de": "Vorfalltyp", "fr": "Type d'incident", "es": "Tipo de incidente", "pl": "Typ incydentu"},
    "Location": {"de": "Standort", "fr": "Emplacement", "es": "Ubicación", "pl": "Lokalizacja"},
    "Severity": {"de": "Schweregrad", "fr": "Gravité", "es": "Gravedad", "pl": "Powaga"},
    "Resolved": {"de": "Gelöst", "fr": "Résolu", "es": "Resuelto", "pl": "Rozwiązane"},
    
    # Common actions
    "Save": {"de": "Speichern", "fr": "Enregistrer", "es": "Guardar", "pl": "Zapisz"},
    "Cancel": {"de": "Abbrechen", "fr": "Annuler", "es": "Cancelar", "pl": "Anuluj"},
    "Delete": {"de": "Löschen", "fr": "Supprimer", "es": "Eliminar", "pl": "Usuń"},
    "Edit": {"de": "Bearbeiten", "fr": "Modifier", "es": "Editar", "pl": "Edytuj"},
    "View": {"de": "Ansehen", "fr": "Voir", "es": "Ver", "pl": "Zobacz"},
    "Back": {"de": "Zurück", "fr": "Retour", "es": "Volver", "pl": "Wstecz"},
    "Search": {"de": "Suchen", "fr": "Rechercher", "es": "Buscar", "pl": "Szukaj"},
    "Filter": {"de": "Filtern", "fr": "Filtrer", "es": "Filtrar", "pl": "Filtruj"},
    "Actions": {"de": "Aktionen", "fr": "Actions", "es": "Acciones", "pl": "Akcje"},
    "Details": {"de": "Details", "fr": "Détails", "es": "Detalles", "pl": "Szczegóły"},
    
    # Messages
    "Are you sure you want to delete this?": {
        "de": "Möchten Sie dies wirklich löschen?",
        "fr": "Êtes-vous sûr de vouloir supprimer ceci?",
        "es": "¿Está seguro de que desea eliminar esto?",
        "pl": "Czy na pewno chcesz to usunąć?"
    },
    "Successfully saved": {
        "de": "Erfolgreich gespeichert",
        "fr": "Enregistré avec succès",
        "es": "Guardado exitosamente",
        "pl": "Pomyślnie zapisano"
    },
    "Successfully deleted": {
        "de": "Erfolgreich gelöscht",
        "fr": "Supprimé avec succès",
        "es": "Eliminado exitosamente",
        "pl": "Pomyślnie usunięto"
    },
    "No items found": {
        "de": "Keine Elemente gefunden",
        "fr": "Aucun élément trouvé",
        "es": "No se encontraron elementos",
        "pl": "Nie znaleziono elementów"
    },
}

base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')

print("Adding comprehensive translations for all pages...")
print("="*60)

for lang in ['de', 'fr', 'es', 'pl']:
    po_file = base_dir / f"{lang}/LC_MESSAGES/django.po"
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    added = 0
    for english, trans_dict in all_translations.items():
        if lang not in trans_dict:
            continue
        
        translation = trans_dict[lang]
        
        # Check if already exists
        if f'msgid "{english}"' not in content:
            # Add new entry
            new_entry = f'\nmsgid "{english}"\nmsgstr "{translation}"\n'
            content = content.rstrip() + new_entry + '\n'
            added += 1
    
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {lang.upper()}: Added {added} new translations")

print("="*60)
print(f"\n✅ All translations added for {len(all_translations)} strings!")
print("\nNext: Compile .mo files with:")
print("  msgfmt -o locale/{lang}/LC_MESSAGES/django.mo locale/{lang}/LC_MESSAGES/django.po")
