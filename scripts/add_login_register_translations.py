#!/usr/bin/env python
"""Add login/register page translations to all language .po files"""
from pathlib import Path

# New translations for login/register pages
new_translations = {
    # Login page
    "Login - Car Fleet Management": {
        "de": "Anmelden - Fahrzeugflottenverwaltung",
        "fr": "Connexion - Gestion de flotte automobile",
        "es": "Iniciar sesión - Gestión de flota de vehículos",
        "pl": "Logowanie - System zarządzania flotą samochodową"
    },
    "Welcome Back": {
        "de": "Willkommen zurück",
        "fr": "Bienvenue",
        "es": "Bienvenido de nuevo",
        "pl": "Witamy ponownie"
    },
    "Sign in to access your fleet dashboard": {
        "de": "Melden Sie sich an, um auf Ihr Flotten-Dashboard zuzugreifen",
        "fr": "Connectez-vous pour accéder à votre tableau de bord de flotte",
        "es": "Inicie sesión para acceder a su panel de flota",
        "pl": "Zaloguj się, aby uzyskać dostęp do panelu floty"
    },
    "Invalid username or password. Please try again.": {
        "de": "Ungültiger Benutzername oder Passwort. Bitte versuchen Sie es erneut.",
        "fr": "Nom d'utilisateur ou mot de passe invalide. Veuillez réessayer.",
        "es": "Nombre de usuario o contraseña inválidos. Por favor, inténtelo de nuevo.",
        "pl": "Nieprawidłowa nazwa użytkownika lub hasło. Spróbuj ponownie."
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
        "es": "Iniciar sesión",
        "pl": "Zaloguj się"
    },
    "Don't have an account?": {
        "de": "Haben Sie kein Konto?",
        "fr": "Vous n'avez pas de compte?",
        "es": "¿No tienes una cuenta?",
        "pl": "Nie masz konta?"
    },
    "Register here": {
        "de": "Hier registrieren",
        "fr": "S'inscrire ici",
        "es": "Regístrese aquí",
        "pl": "Zarejestruj się tutaj"
    },
    
    # Register page
    "Register - Car Fleet Management": {
        "de": "Registrieren - Fahrzeugflottenverwaltung",
        "fr": "S'inscrire - Gestion de flotte automobile",
        "es": "Registrarse - Gestión de flota de vehículos",
        "pl": "Rejestracja - System zarządzania flotą samochodową"
    },
    "Create Account": {
        "de": "Konto erstellen",
        "fr": "Créer un compte",
        "es": "Crear cuenta",
        "pl": "Utwórz konto"
    },
    "Join the fleet management platform": {
        "de": "Treten Sie der Flottenverwaltungsplattform bei",
        "fr": "Rejoignez la plateforme de gestion de flotte",
        "es": "Únase a la plataforma de gestión de flotas",
        "pl": "Dołącz do platformy zarządzania flotą"
    },
    "Please correct the errors below.": {
        "de": "Bitte korrigieren Sie die folgenden Fehler.",
        "fr": "Veuillez corriger les erreurs ci-dessous.",
        "es": "Por favor corrija los errores a continuación.",
        "pl": "Proszę poprawić poniższe błędy."
    },
    "Already have an account?": {
        "de": "Haben Sie bereits ein Konto?",
        "fr": "Vous avez déjà un compte?",
        "es": "¿Ya tienes una cuenta?",
        "pl": "Masz już konto?"
    },
    "Login here": {
        "de": "Hier anmelden",
        "fr": "Se connecter ici",
        "es": "Inicie sesión aquí",
        "pl": "Zaloguj się tutaj"
    },
}

base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')

for lang in ['de', 'fr', 'es', 'pl']:
    po_file = base_dir / f"{lang}/LC_MESSAGES/django.po"
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    added = 0
    for english, trans_dict in new_translations.items():
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
    
    print(f"✅ {lang.upper()}: Added {added} login/register translations")

print("\n✅ All login/register translations added!")
