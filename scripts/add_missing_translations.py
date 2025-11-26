#!/usr/bin/env python
"""Add missing translations to Polish django.po file"""
import re

po_file = r'd:\REPOS\fleet_mgmt_django\locale\pl\LC_MESSAGES\django.po'

# Read the file
with open(po_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Translations to add
translations = {
    "Welcome to Fleet Management": "Witamy w zarządzaniu flotą",
    "Manage your vehicle fleet with ease and efficiency": "Zarządzaj swoją flotą pojazdów z łatwością i wydajnością",
    "System Overview": "Przegląd systemu",
    "System Online": "System online",
    "Quick Actions": "Szybkie działania",
    "Register new vehicle": "Zarejestruj nowy pojazd",
    "Report incident": "Zgłoś incydent",
    "Schedule service": "Zaplanuj serwis",
    "Recent Activity": "Ostatnia aktywność",
    "System maintenance completed successfully": "Konserwacja systemu zakończona pomyślnie",
    "New fleet regulations update available": "Dostępna aktualizacja przepisów dotyczących floty",
    "3 vehicles due for inspection this week": "3 pojazdy wymagają przeglądu w tym tygodniu",
}

# Add missing translations
for english, polish in translations.items():
    # Check if translation exists
    pattern = f'msgid "{re.escape(english)}"'
    if pattern in content:
        # Check if it has a translation
        msgid_pattern = f'msgid "{re.escape(english)}"\nmsgstr ""'
        if msgid_pattern in content:
            # Add translation
            replacement = f'msgid "{english}"\nmsgstr "{polish}"'
            content = content.replace(msgid_pattern, replacement)
            print(f"✅ Added translation for: {english}")
        else:
            print(f"⏭️  Already translated: {english}")
    else:
        # Add new entry
        new_entry = f'\nmsgid "{english}"\nmsgstr "{polish}"\n'
        # Add before the last line
        content = content.rstrip() + new_entry + '\n'
        print(f"➕ Added new entry for: {english}")

# Write back
with open(po_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Polish translations updated!")
print("Now run: python manage.py compilemessages")
