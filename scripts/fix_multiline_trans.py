#!/usr/bin/env python
"""Fix all multi-line {% trans %} tags in templates"""
import re

def fix_multiline_trans_tags(filepath):
    """Fix multi-line {% trans %} tags by putting them on single lines"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match {% trans "..." %} split across lines
    # This matches: {% trans "text
    #                %} or similar patterns
    pattern = r'{%\s*trans\s+"([^"]*?)"\s*\n\s*%}'
    replacement = r'{% trans "\1" %}'
    
    fixed_content = re.sub(pattern, replacement, content)
    
    # Also fix cases where the opening tag is split
    pattern2 = r'{%\s*trans\s+\n\s*"([^"]*?)"\s*%}'
    fixed_content = re.sub(pattern2, r'{% trans "\1" %}', fixed_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed: {filepath}")

# Fix both templates
fix_multiline_trans_tags(r'd:\REPOS\fleet_mgmt_django\CarFleetManagement\templates\base_v2.html')
fix_multiline_trans_tags(r'd:\REPOS\fleet_mgmt_django\CarFleetManagement\templates\home.html')

print("\n✅ All multi-line {% trans %} tags fixed!")
