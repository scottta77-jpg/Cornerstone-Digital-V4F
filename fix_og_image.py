import os
import glob

html_files = glob.glob('**/*.html', recursive=True)
active_files = [f for f in html_files if not f.startswith('site-reference') and not f.startswith('node_modules')]

for file_path in active_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('content="/assets/images/cornerstone-logo-3.png"', 'content="https://cornerstonedg.com/assets/images/cornerstone-logo-3.png"')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(active_files)} files with absolute og:image URL.")
