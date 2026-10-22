import os
import glob

html_files = glob.glob('**/*.html', recursive=True)
active_files = [f for f in html_files if not f.startswith('site-reference') and not f.startswith('node_modules')]

for file_path in active_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the old OG image with the new compiled one
    content = content.replace('content="https://cornerstonedg.com/assets/images/cornerstone-logo-3.png"', 'content="https://cornerstonedg.com/assets/images/cornerstone-og-preview.png"')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(active_files)} files with new Cornerstone OG image.")
