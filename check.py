import glob
files = glob.glob("**/*.html", recursive=True)
for f in files:
    content = open(f).read()
    if 'gsap.min.js' not in content:
        print(f"{f} lacks GSAP")
