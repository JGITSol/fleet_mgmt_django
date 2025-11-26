import re

# Read the file
with open('CarFleetManagement/templates/base_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix multi-line {% trans %} tags
# Pattern: {% trans "text"\n    %}
# Replace with: {% trans "text" %}

# Fix pattern 1: {% trans "text"\n    %}
content = re.sub(
    r'{%\s*trans\s+"([^"]+)"\s*\n\s*%}',
    r'{% trans "\1" %}',
    content
)

# Fix pattern 2: {% trans 'text'\n    %}
content = re.sub(
    r"{%\s*trans\s+'([^']+)'\s*\n\s*%}",
    r"{% trans '\1' %}",
    content
)

# Fix pattern 3: {% trans\n    "text" %}
content = re.sub(
    r'{%\s*trans\s*\n\s*"([^"]+)"\s*%}',
    r'{% trans "\1" %}',
    content
)

# Fix pattern 4: {% trans\n    'text' %}
content = re.sub(
    r"{%\s*trans\s*\n\s*'([^']+)'\s*%}",
    r"{% trans '\1' %}",
    content
)

# Write back
with open('CarFleetManagement/templates/base_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed multi-line {% trans %} tags in base_v2.html")

# Show what was fixed
print("\nChecking for remaining multi-line trans tags...")
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '{% trans' in line and not '%}' in line:
        print(f"⚠️  Line {i}: {line.strip()}")
        if i < len(lines):
            print(f"    Line {i+1}: {lines[i].strip()}")
