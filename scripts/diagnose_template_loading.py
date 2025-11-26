import os
from pathlib import Path
from django.template.loader import get_template
from django.conf import settings

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
import django
django.setup()

output_lines = []

# Get the template
try:
    template = get_template('base_v2.html')
    output_lines.append(f"Template origin: {template.origin}")
    output_lines.append(f"Template name: {template.origin.name}")
    output_lines.append(f"Template path: {template.origin.template_name}")
    
    # Read the actual file Django is using
    with open(template.origin.name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        output_lines.append(f"\nLine 71 content:")
        output_lines.append(f"{lines[70]}")
        
        # Search for the problematic pattern
        output_lines.append(f"\nAll lines containing 'language.code':")
        for i, line in enumerate(lines, 1):
            if 'language.code' in line and 'LANGUAGE_CODE' in line:
                output_lines.append(f"Line {i}: {line.strip()}")
                
except Exception as e:
    output_lines.append(f"Error: {e}")
    import traceback
    output_lines.append(traceback.format_exc())

# Write to file
with open('template_diagnostic_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Diagnostic output written to template_diagnostic_output.txt")
