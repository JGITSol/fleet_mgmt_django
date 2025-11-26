import os
import re
from pathlib import Path

def check_empty_translations():
    base_dir = Path('locale')
    languages = ['de', 'fr', 'es', 'pl', 'en']
    
    print(f"{'Language':<10} | {'Empty msgstr':<15} | {'Total msgid':<15}")
    print("-" * 45)
    
    for lang in languages:
        po_file = base_dir / lang / 'LC_MESSAGES' / 'django.po'
        if not po_file.exists():
            print(f"{lang:<10} | {'File not found':<15} | {'-':<15}")
            continue
            
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Count empty msgstr (excluding header)
        # Pattern: msgid "..." followed by msgstr ""
        # We need to be careful not to count the header which also has msgid "" and msgstr ""
        
        # Simple approach: find all msgstr "" and subtract 1 (for header) if it exists
        empty_matches = re.findall(r'msgstr ""', content)
        total_empty = len(empty_matches)
        
        # Check if header is present (it usually is)
        if 'msgid ""\nmsgstr ""' in content:
            total_empty -= 1
            
        # Count total msgids
        total_msgids = len(re.findall(r'^msgid "', content, re.MULTILINE))
        
        print(f"{lang:<10} | {total_empty:<15} | {total_msgids:<15}")

if __name__ == "__main__":
    check_empty_translations()
