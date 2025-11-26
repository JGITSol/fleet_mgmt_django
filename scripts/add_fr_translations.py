#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add French translations to django.po file for ALL user-facing strings"""

import re

po_file_path = r'd:\REPOS\fleet_mgmt_django\locale\fr\LC_MESSAGES\django.po'

# Read the file
with open(po_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define ALL translations needed for complete coverage
translations = {
    # Navigation & Branding
    'FleetManager': 'Gestionnaire de Flotte',
    'Home Page': 'Page d\'Accueil',
    'Home': 'Accueil',
    'Login': 'Connexion',
    'Register': 'S\'inscrire',
    'Logout': 'Déconnexion',
    'Admin': 'Administrateur',
    'Profile': 'Profil',
    
    # Hero Section
    'Next-Gen Fleet Management': 'Gestion de Flotte Nouvelle Génération',
    'Streamline your operations, track maintenance, and manage your fleet with our premium, intelligent solution.': 
        'Rationalisez vos opérations, suivez la maintenance et gérez votre flotte avec notre solution intelligente premium.',
    'Get Started': 'Commencer',
    'Manage Fleet': 'Gérer la Flotte',
    'View Maintenance': 'Voir la Maintenance',
    
    # Features
    'Real-time Tracking': 'Suivi en Temps Réel',
    'Monitor your fleet\'s location and status in real-time with our advanced GPS integration systems.':
        'Surveillez l\'emplacement et le statut de votre flotte en temps réel avec nos systèmes d\'intégration GPS avancés.',
    'Smart Maintenance': 'Maintenance Intelligente',
    'Predictive maintenance alerts and scheduling to keep your vehicles running at peak performance.':
        'Alertes de maintenance prédictive et planification pour maintenir vos véhicules à des performances optimales.',
    'Analytics Dashboard': 'Tableau de Bord Analytique',
    'Comprehensive insights into fuel usage, driver behavior, and operational costs.':
        'Aperçus complets de l\'utilisation du carburant, du comportement des conducteurs et des coûts opérationnels.',
    
    # System Overview
    'System Overview': 'Aperçu du Système',
    'System Online': 'Système En Ligne',
    'Quick Actions': 'Actions Rapides',
    'Register new vehicle': 'Enregistrer un nouveau véhicule',
    'Report incident': 'Signaler un incident',
    'Schedule service': 'Planifier un service',
    'Recent Activity': 'Activité Récente',
    'System maintenance completed successfully': 'Maintenance du système terminée avec succès',
    'New fleet regulations update available': 'Nouvelle mise à jour des réglementations de flotte disponible',
    '3 vehicles due for inspection this week': '3 véhicules à inspecter cette semaine',
    
    # Login Page
    'Welcome Back': 'Bon Retour',
    'Sign In': 'Se Connecter',
    'Sign in to access your fleet dashboard': 'Connectez-vous pour accéder à votre tableau de bord de flotte',
    'Username': 'Nom d\'utilisateur',
    'Password': 'Mot de passe',
    'Invalid username or password. Please try again.': 'Nom d\'utilisateur ou mot de passe invalide. Veuillez réessayer.',
    'Register here': 'S\'inscrire ici',
    'Don\'t have an account?': 'Vous n\'avez pas de compte?',
    
    # Footer
    'Premium Fleet Management Solution': 'Solution Premium de Gestion de Flotte',
    'Car Fleet Management System': 'Système de Gestion de Flotte Automobile',
    'Toggle Theme': 'Basculer le Thème',
    
    # Vehicles
    'Vehicles': 'Véhicules',
    'Maintenance': 'Maintenance',
    'Emergency': 'Urgence',
    
    # General
    'Car Fleet Management': 'Gestion de Flotte Automobile',
    'Home - Car Fleet Management': 'Accueil - Gestion de Flotte Automobile',
    'Login - Car Fleet Management': 'Connexion - Gestion de Flotte Automobile',
}

# Apply translations
count = 0
for english, french in translations.items():
    # Find msgid "english"\nmsgstr ""
    pattern = rf'(msgid "{re.escape(english)}"\s*\nmsgstr ")("")'
    if re.search(pattern, content):
        replacement = rf'\1{french}\2'
        content = re.sub(pattern, replacement, content)
        count += 1

# Write back
with open(po_file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully added {count} French translations to django.po")
print(f"Total translations defined: {len(translations)}")
