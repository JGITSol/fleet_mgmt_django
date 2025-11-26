
import os

def update_templates(root_dir):
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content.replace("{% extends 'base.html' %}", "{% extends 'base_v2.html' %}")
                    new_content = new_content.replace('{% extends "base.html" %}', '{% extends "base_v2.html" %}')
                    
                    if content != new_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated {filepath}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_templates(r"d:\REPOS\fleet_mgmt_django")
