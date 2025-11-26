#!/usr/bin/env python
"""Fix .po file headers and ensure proper format"""
from pathlib import Path

header_template = '''# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: \\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-11-24 06:00+0000\\n"
"PO-Revision-Date: 2025-11-24 06:00+0000\\n"
"Last-Translator: Auto <auto@example.com>\\n"
"Language-Team: {language}\\n"
"Language: {lang_code}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

'''

base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')

lang_names = {
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'pl': 'Polish'
}

for lang_code, lang_name in lang_names.items():
    po_file = base_dir / f"{lang_code}/LC_MESSAGES/django.po"
    
    if not po_file.exists():
        print(f"❌ {lang_code}: File not found")
        continue
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove old header if exists
    if content.startswith('#'):
        # Find first msgid
        first_msgid = content.find('\nmsgid "')
        if first_msgid > 0:
            content = content[first_msgid+1:]
    
    # Add proper header
    header = header_template.format(language=lang_name, lang_code=lang_code)
    new_content = header + content
    
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {lang_code.upper()}: Header fixed")

print("\n✅ All headers fixed!")
