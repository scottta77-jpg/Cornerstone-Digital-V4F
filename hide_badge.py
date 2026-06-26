import glob
import os

files = glob.glob("**/*.html", recursive=True)

badge_css = """
    <style>
      /* Hide the Made in Webflow badge */
      .w-webflow-badge {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
      }
    </style>
"""

for f in files:
    if 'components/' in f or 'site-reference/' in f:
        continue

    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    if 'Hide the Made in Webflow badge' not in content:
        content = content.replace('</head>', badge_css + '  </head>')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated: {f}")

print("Done hiding webflow badge.")
