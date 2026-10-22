import os
import glob

html_files = glob.glob('**/*.html', recursive=True)
active_files = [f for f in html_files if not f.startswith('site-reference') and not f.startswith('node_modules')]

for file_path in active_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Webflow comment
    content = content.replace('<!-- This site was created in Webflow. https://webflow.com -->', '')
    
    # 2. Meta description
    content = content.replace('Cornerstone Digital is a modern Webflow agency template for studios, freelancers, and digital agencies.', 'Cornerstone Digital is a digital growth agency helping local businesses attract more customers and scale faster through smart design and automation.')
    
    # 3. Meta title
    content = content.replace('Cornerstone Digital  - Webflow HTML Website Template', 'Cornerstone Digital | Growth by Design')
    
    # 4. Generator
    content = content.replace('content="Webflow" name="generator"', 'content="Cornerstone Digital" name="generator"')
    
    # 5. OG Image
    content = content.replace('https://cdn.prod.website-files.com/69f5c8889d124099c0296270/6a1189df3a2d9d72aabba231_open_graph_preview%20(1).jpg', '/assets/images/cornerstone-logo-3.png')
    
    # 6. Any other "Webflow" in meta tags or titles
    content = content.replace('Webflow development', 'Web development')
    content = content.replace('Webflow,', 'Web development,')
    
    # 7. Webflow badge comment
    content = content.replace('/* Hide the Made in Webflow badge */', '')
    
    # 8. Webflow IX3 comment
    content = content.replace('/* Comprehensive Webflow IX3 animation replacement */', '/* Comprehensive animation replacement */')
    content = content.replace('/* Safety-net visibility for Webflow IX3 animated elements.', '/* Safety-net visibility for animated elements.')
    
    # 9. Olyyx
    content = content.replace('Olyyx', 'Cornerstone Digital')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(active_files)} files.")
