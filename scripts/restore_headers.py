from pathlib import Path

HEADER = r'''msgid ""
msgstr ""
"Project-Id-Version: \n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2025-11-24 14:26+0100\n"
"PO-Revision-Date: 2025-11-24 06:00+0000\n"
"Last-Translator: Auto <auto@example.com>\n"
"Language-Team: {language}\n"
"Language: {lang_code}\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: {plural_forms}\n"

'''

PLURAL_FORMS = {
    'en': 'nplurals=2; plural=(n != 1);',
    'de': 'nplurals=2; plural=(n != 1);',
    'fr': 'nplurals=2; plural=(n > 1);',
    'es': 'nplurals=2; plural=(n != 1);',
    'pl': 'nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);'
}

LANG_NAMES = {
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'pl': 'Polish'
}

def restore_header(po_file, lang_code):
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'msgid ""\nmsgstr ""' in content:
        print(f"✅ {lang_code}: Header already exists")
        return
        
    print(f"⚠️  {lang_code}: Restoring header...")
    
    # Find where to insert (after comments)
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines):
        if not line.startswith('#'):
            insert_idx = i
            break
            
    header = HEADER.format(
        language=LANG_NAMES.get(lang_code, 'Unknown'),
        lang_code=lang_code,
        plural_forms=PLURAL_FORMS.get(lang_code, 'nplurals=2; plural=(n != 1);')
    )
    
    lines.insert(insert_idx, header)
    
    with open(po_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print(f"✅ {lang_code}: Header restored")

def main():
    base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')
    for lang in ['de', 'fr', 'es', 'pl', 'en']:
        po_file = base_dir / lang / 'LC_MESSAGES' / 'django.po'
        if po_file.exists():
            restore_header(po_file, lang)

if __name__ == "__main__":
    main()
