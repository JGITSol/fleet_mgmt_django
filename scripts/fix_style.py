
import os

file_path = r'D:\REPOS\fleet_mgmt_django\CarFleetManagement\static\css\style.css'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Part 1: Keep up to line 195 (index 195 is line 196, so up to index 195 means 0..194)
# Line 195 in file is index 194.
# Let's check the content to be sure.
# Line 195 is "    }"
part1 = lines[:196] 

# Part 2: Add missing h1 rule and close media query
part2 = [
    "\n",
    "    h1 {\n",
    "        font-size: 2.5rem;\n",
    "    }\n",
    "}\n",
    "\n"
]

# Part 3: Extract Components and dedent
# Find start of components
start_index = -1
for i, line in enumerate(lines):
    if "/* Components */" in line:
        start_index = i
        break

if start_index == -1:
    print("Could not find Components section!")
    exit(1)

part3 = []
for line in lines[start_index:]:
    # Dedent by 8 spaces if possible, or 12 if it was deeply nested
    # The view showed 8 spaces for .navbar
    if line.startswith("        "):
        part3.append(line[8:])
    elif line.startswith("            "): # In case of deeper nesting
        part3.append(line[8:])
    else:
        # Keep empty lines or lines with less indentation as is (or strip leading whitespace if it's just indentation)
        # But wait, if it's "    /* Components */", it has 4 spaces?
        # In the view: "377:         /* Components */" -> 8 spaces?
        # Let's just strip 8 spaces if they exist.
        if len(line) > 8 and line[:8].isspace():
             part3.append(line[8:])
        else:
             part3.append(line.lstrip()) # Fallback

# Combine
new_content = "".join(part1 + part2 + part3)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed style.css")
