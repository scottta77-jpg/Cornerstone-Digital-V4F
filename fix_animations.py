import glob
import re

files = glob.glob("**/*.html", recursive=True)

fade_up_script = """
    <script>
      document.addEventListener("DOMContentLoaded", () => {
        if (!window.gsap) return;
        gsap.registerPlugin(ScrollTrigger);
        gsap.utils.toArray('[fade-up="true"]').forEach((el) => {
          gsap.fromTo(el, 
            { opacity: 0, y: 40 },
            {
              opacity: 1,
              y: 0,
              duration: 1,
              ease: "power3.out",
              scrollTrigger: {
                trigger: el,
                start: "top 85%",
                toggleActions: "play none none none"
              }
            }
          );
        });
      });
    </script>
"""

for f in files:
    if 'components/' in f or 'site-reference/' in f:
        continue

    with open(f, 'r') as file:
        content = file.read()

    changed = False

    # 1. Enable Cube animation on mobile
    if 'mm.add("(min-width: 992px)", () => {' in content:
        content = content.replace('mm.add("(min-width: 992px)", () => {', 'mm.add("(min-width: 0px)", () => {')
        changed = True

    # 2. Enable Testimonial Drag on mobile
    if 'if (window.innerWidth <= 991) return;' in content:
        content = content.replace('if (window.innerWidth <= 991) return;', '// if (window.innerWidth <= 991) return;')
        changed = True

    # 3. Add fade-up animation script if fade-up attributes exist
    if 'fade-up="true"' in content and 'gsap.utils.toArray(\'[fade-up="true"]\')' not in content:
        # insert before </body>
        content = content.replace('</body>', fade_up_script + '\n</body>')
        changed = True

    if changed:
        with open(f, 'w') as file:
            file.write(content)
        print(f"Updated animations for {f}")

print("Done!")
