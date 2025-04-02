# Localization Files

This directory contains all translation files for the Car Fleet Manager system. The structure follows Django's localization conventions with separate directories for each language.

## Supported Languages
- English (en)
- German (de)
- Spanish (es)
- French (fr)
- Polish (pl)

## File Structure
Each language directory contains:
- `LC_MESSAGES/django.po` - Main translation file for UI strings
- `legal/` - Legal documents (terms, privacy policy, etc.)
- `marketing/` - Marketing materials translations

## Adding New Languages
1. Create a new directory with the language code (ISO 639-1)
2. Add `LC_MESSAGES/django.po` file
3. Create `legal` and `marketing` subdirectories
4. Run `django-admin compilemessages` to compile translations