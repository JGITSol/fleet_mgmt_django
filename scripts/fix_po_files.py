#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct fix for django.po files - adds ALL missing translations
"""

def fix_po_file(lang_code, translations):
    """Fix a .po file by adding translations"""
    po_file = f'd:\\REPOS\\fleet_mgmt_django\\locale\\{lang_code}\\LC_MESSAGES\\django.po'
    
    print(f"\nFixing {lang_code.upper()} translations...")
    
    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  ❌ File not found: {po_file}")
        return 0
    
    # Find and update translations
    updated = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for msgid lines
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            # Extract the msgid value
            msgid_value = line[7:-2]  # Remove 'msgid "' and '"\n'
            
            # Check if next line is empty msgstr
            if i + 1 < len(lines) and lines[i + 1].startswith('msgstr ""'):
                # Check if we have a translation for this
                if msgid_value in translations:
                    # Replace the empty msgstr with the translation
                    lines[i + 1] = f'msgstr "{translations[msgid_value]}"\n'
                    updated += 1
        
        i += 1
    
    # Write back
    with open(po_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"  ✅ Updated {updated} translations")
    return updated

# French translations
french_translations = {
    'Home': 'Accueil',
    'Login': 'Connexion',
    'Register': 'S\'inscrire',
    'Logout': 'Déconnexion',
    'Admin': 'Administrateur',
    'Profile': 'Profil',
    'Vehicles': 'Véhicules',
    'Maintenance': 'Maintenance',
    'Emergency': 'Urgence',
    'Fleet Management': 'Gestion de Flotte',
    'Change Language': 'Changer de Langue',
}

# Polish translations
polish_translations = {
    'Home': 'Strona Główna',
    'Login': 'Logowanie',
    'Register': 'Rejestracja',
    'Logout': 'Wyloguj',
    'Admin': 'Administrator',
    'Profile': 'Profil',
    'Vehicles': 'Pojazdy',
    'Maintenance': 'Konserwacja',
    'Emergency': 'Awaria',
    'Fleet Management': 'Zarządzanie Flotą',
    'Change Language': 'Zmień Język',
}

print("="*60)
print("DIRECT PO FILE FIX")
print("="*60)

fr_count = fix_po_file('fr', french_translations)
pl_count = fix_po_file('pl', polish_translations)

print(f"\n{'='*60}")
print(f"Total: {fr_count + pl_count} translations added")
print(f"{'='*60}")
