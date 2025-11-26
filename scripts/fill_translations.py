"""
Fill ALL empty translations in .po files for all 4 languages
"""

import os
import re
from pathlib import Path

# Complete translation dictionary
TRANSLATIONS = {
    # Page titles
    "Car Fleet Management": {"pl": "Zarządzanie Flotą Samochodową", "fr": "Gestion de Flotte Automobile", "es": "Gestión de Flota de Vehículos", "de": "Fahrzeugflottenmanagement"},
    "Fleet Management": {"pl": "Zarządzanie Flotą", "fr": "Gestion de Flotte", "es": "Gestión de Flota", "de": "Flottenmanagement"},
    
    # Navigation
    "Home": {"pl": "Strona główna", "fr": "Accueil", "es": "Inicio", "de": "Startseite"},
    "FleetManager": {"pl": "Menedżer Floty", "fr": "Gestionnaire de Flotte", "es": "Gestor de Flota", "de": "Flottenmanager"},
    "Vehicles": {"pl": "Pojazdy", "fr": "Véhicules", "es": "Vehículos", "de": "Fahrzeuge"},
    "Maintenance": {"pl": "Konserwacja", "fr": "Maintenance", "es": "Mantenimiento", "de": "Wartung"},
    "Emergency": {"pl": "Nagłe wypadki", "fr": "Urgence", "es": "Emergencia", "de": "Notfall"},
    "Admin": {"pl": "Administrator", "fr": "Admin", "es": "Admin", "de": "Admin"},
    "Profile": {"pl": "Profil", "fr": "Profil", "es": "Perfil", "de": "Profil"},
    "Login": {"pl": "Zaloguj się", "fr": "Connexion", "es": "Iniciar sesión", "de": "Anmelden"},
    "Logout": {"pl": "Wyloguj się", "fr": "Déconnexion", "es": "Cerrar sesión", "de": "Abmelden"},
    "Register": {"pl": "Zarejestruj się", "fr": "S'inscrire", "es": "Registrarse", "de": "Registrieren"},
    "Change Language": {"pl": "Zmień język", "fr": "Changer de langue", "es": "Cambiar idioma", "de": "Sprache ändern"},
    "Toggle Theme": {"pl": "Przełącz motyw", "fr": "Changer de thème", "es": "Cambiar tema", "de": "Design wechseln"},
    
    # Footer
    "Premium Fleet Management Solution": {"pl": "Rozwiązanie Premium do Zarządzania Flotą", "fr": "Solution Premium de Gestion de Flotte", "es": "Solución Premium de Gestión de Flota", "de": "Premium-Flottenmanagementsolution"},
    "Car Fleet Management System": {"pl": "System Zarządzania Flotą Samochodową", "fr": "Système de Gestion de Flotte Automobile", "es": "Sistema de Gestión de Flota de Vehículos", "de": "Fahrzeugflottenmanagementsystem"},
}

def fill_translations(po_file_path, language_code):
    """Fill all empty msgstr entries in a .po file"""
    if not os.path.exists(po_file_path):
        print(f"⚠️  File not found: {po_file_path}")
        return 0
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove fuzzy flag from header
    content = content.replace('#, fuzzy\nmsgid ""', 'msgid ""')
    
    updated_count = 0
    
    # Pattern to match msgid/msgstr pairs with empty msgstr
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
    
    return updated_count

def main():
    base_dir = Path('locale')
    
    languages = {
        'pl': 'Polish',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German'
    }
    
    print("=" * 60)
    print("Filling All Empty Translations")
    print("=" * 60)
    
    total_updated = 0
    
    for lang_code, lang_name in languages.items():
        print(f"\n📝 Processing {lang_name} ({lang_code})...")
        po_file = base_dir / lang_code / 'LC_MESSAGES' / 'django.po'
        count = fill_translations(str(po_file), lang_code)
        print(f"✅ Filled {count} translations in {lang_code}.po")
        total_updated += count
    
    print("\n" + "=" * 60)
    print(f"✅ Translation filling complete!")
    print(f"📊 Total translations filled: {total_updated}")
    print(f"📚 Translation dictionary size: {len(TRANSLATIONS)} strings")
    print(f"🌍 Languages: {', '.join(languages.values())}")
    print("=" * 60)

if __name__ == '__main__':
    main()
