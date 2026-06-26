import re

with open('index.html', 'r') as f:
    idx = f.read()

with open('about/index.html', 'r') as f:
    abt = f.read()

idx_scripts = re.findall(r'<script.*?</script>', idx, re.DOTALL)
abt_scripts = re.findall(r'<script.*?</script>', abt, re.DOTALL)

print("index.html has", len(idx_scripts), "scripts")
print("about/index.html has", len(abt_scripts), "scripts")

for i, script in enumerate(idx_scripts):
    if script not in abt_scripts:
        print(f"\nMissing in about/index.html (from index.html script #{i}):")
        print(script[:200] + "...")
