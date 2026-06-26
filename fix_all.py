import os
import glob
import re

files = glob.glob("**/*.html", recursive=True)

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the Webflow IX2 hidden style block
    content = re.sub(r'<style>\s*html\.w-mod-js:not\(\.w-mod-ix3\).*?visibility: hidden !important;\s*}\s*</style>', '', content, flags=re.DOTALL)

    # 2. Fix 100vh in the menu script
    content = content.replace('menuContent.style.height = "100vh";', 'menuContent.style.height = "100dvh";')

    # 3. Fix hover items for touch devices in GSAP script
    gsap_hover = """
        // Initial State
        if (window.matchMedia("(hover: none)").matches) {
          gsap.set(btn, { opacity: 1, transformStyle: "flat" });
          return;
        }
        gsap.set(btn, {"""
    content = content.replace('// Initial State\n        gsap.set(btn, {', gsap_hover)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fixed HTML files!")
