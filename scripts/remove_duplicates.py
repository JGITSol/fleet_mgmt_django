#!/usr/bin/env python
"""Remove duplicate msgid entries from .po files"""
import re
from pathlib import Path

def remove_duplicates_from_po(po_file_path):
    """Remove duplicate msgid entries from a .po file"""
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into entries
    entries = re.split(r'\n(?=msgid)', content)
    
    # Keep track of seen msgids
    seen_msgids = set()
    unique_entries = []
    duplicates_removed = 0
    
    for entry in entries:
        # Extract msgid
        msgid_match = re.search(r'msgid\s+"([^"]*)"', entry)
        if msgid_match:
            msgid = msgid_match.group(1)
            if msgid and msgid not in seen_msgids:
                seen_msgids.add(msgid)
                unique_entries.append(entry)
            elif msgid:
                duplicates_removed += 1
        else:
            # Header or other content
            unique_entries.append(entry)
    
    # Rejoin
    new_content = '\n'.join(unique_entries)
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return duplicates_removed

# Fix all language files
base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')

print("Removing duplicates from .po files...")
print("="*50)

for lang in ['de', 'fr', 'es', 'pl']:
    po_file = base_dir / f"{lang}/LC_MESSAGES/django.po"
    if po_file.exists():
        removed = remove_duplicates_from_po(po_file)
        print(f"✅ {lang.upper()}: Removed {removed} duplicates")
    else:
        print(f"❌ {lang.upper()}: File not found")

print("="*50)
print("\n✅ Duplicates removed!")
