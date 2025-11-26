# Locale Directory

This directory contains translation files for the Car Fleet Management application.

## Structure

The locale directory is organized by language code:

```
locale/
├── en/
│   └── LC_MESSAGES/
│       ├── django.mo
│       └── django.po
├── es/
│   └── LC_MESSAGES/
│       ├── django.mo
│       └── django.po
├── fr/
│   └── LC_MESSAGES/
│       ├── django.mo
│       └── django.po
└── de/
    └── LC_MESSAGES/
        ├── django.mo
        └── django.po
```

## Translation Process

1. Mark strings for translation in Python code using `gettext` or `gettext_lazy`:
   ```python
   from django.utils.translation import gettext_lazy as _
   message = _('Welcome to Car Fleet Manager')
   ```

2. Mark strings for translation in templates using the `{% translate %}` tag:
   ```html
   {% load i18n %}
   <h1>{% translate "Welcome to Car Fleet Manager" %}</h1>
   ```

3. Extract messages to be translated:
   ```bash
   python manage.py makemessages -l es
   ```

4. Edit the .po files with translations

5. Compile messages:
   ```bash
   python manage.py compilemessages
   ```

## Adding a New Language

1. Add the language code to the LANGUAGES setting in settings.py
2. Run `python manage.py makemessages -l <language_code>`
3. Translate the strings in the generated .po file
4. Compile the messages with `python manage.py compilemessages`