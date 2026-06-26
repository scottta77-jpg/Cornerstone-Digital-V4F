import os
import glob

script = """
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.querySelector(".menu-btn");
    const menuContent = document.querySelector(".mobile-menu-toggle-content");
    const closeBtn = document.querySelector(".mobile-menu-close-btn-wrap") || document.querySelector(".mobile-menu-close-btn");
    
    if(menuBtn && menuContent) {
      // Ensure it is hidden natively so it doesn't block clicks
      menuContent.style.display = "none";
      menuContent.style.opacity = "0";
      // Ensure high z-index and fixed position for the overlay
      menuContent.style.position = "fixed";
      menuContent.style.top = "0";
      menuContent.style.left = "0";
      menuContent.style.width = "100%";
      menuContent.style.height = "100vh";
      menuContent.style.zIndex = "99999";
      
      menuBtn.addEventListener("click", () => {
        if(window.gsap) {
          gsap.to(menuContent, { display: "block", opacity: 1, duration: 0.3, ease: "power2.out" });
        } else {
          menuContent.style.display = "block";
          menuContent.style.opacity = "1";
        }
      });
      
      if(closeBtn) {
        closeBtn.addEventListener("click", () => {
          if(window.gsap) {
            gsap.to(menuContent, { opacity: 0, duration: 0.3, onComplete: () => {
              menuContent.style.display = "none";
            }});
          } else {
            menuContent.style.display = "none";
            menuContent.style.opacity = "0";
          }
        });
      }
    }
  });
</script>
</body>
"""

files = [
  "./index.html",
  "./about/index.html",
  "./services/index.html",
  "./projects/index.html",
  "./project/ecosphere/index.html",
  "./blogs/index.html",
  "./contact/index.html",
  "./404.html",
  "./404/index.html",
  "./term-of-condition/index.html",
  "./privacy-policy/index.html"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Avoid duplicating if already present
        if 'menuContent.style.display' not in content:
            content = content.replace("</body>", script)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f"Patched {file_path}")
