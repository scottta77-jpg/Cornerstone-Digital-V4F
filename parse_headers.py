import re
with open('/tmp/webflow.html', 'r') as f:
    content = f.read()

matches = re.findall(r'<div class="section-label[^>]*>.*?</div>\s*</div>', content, re.DOTALL)
for i, match in enumerate(matches):
    print(f"--- Header {i} ---")
    print(match[:200])
