#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add Polish translations to django.po file"""

import re

po_file_path = r'd:\REPOS\fleet_mgmt_django\locale\pl\LC_MESSAGES\django.po'

# Read the file
with open(po_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define translations
translations = {
    'FleetManager': 'Zarządzanie Flotą',
    'Home Page': 'Strona Domowa',
    'Car Fleet Management': 'Zarządzanie Flotą Samochodową',
    'Welcome Back': 'Witamy Ponownie',
    'Sign In': 'Zaloguj się',
    'Sign in to access your fleet dashboard': 'Zaloguj się, aby uzyskać dostęp do panelu floty',
    'Username': 'Nazwa użytkownika',
    'Password': 'Hasło',
    'Invalid username or password. Please try again.': 'Nieprawidłowa nazwa użytkownika lub hasło. Spróbuj ponownie.',
    'Register here': 'Zarejestruj się tutaj',
    "Don't have an account?": 'Nie masz konta?',
    'Toggle Theme': 'Przełącz Motyw',
    'Premium Fleet Management Solution': 'Rozwiązanie Premium do Zarządzania Flotą',
    'Car Fleet Management System': 'System Zarządzania Flotą Samochodową',
    'Vehicles': 'Pojazdy',
    'Maintenance': 'Konserwacja',
    'Emergency': 'Awaria',
    'Admin': 'Administrator',
    'Logout': 'Wyloguj',
    'Login': 'Logowanie',
    'Register': 'Rejestracja',
    'Home': 'Strona Główna',
}

# Apply translations
for english, polish in translations.items():
    # Find msgid "english"\nmsgstr ""
    pattern = rf'(msgid "{re.escape(english)}"\s*\nmsgstr ")("")'
    replacement = rf'\1{polish}\2'
    content = re.sub(pattern, replacement, content)

# Write back
with open(po_file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully added {len(translations)} Polish translations to django.po")
