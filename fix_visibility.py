#!/usr/bin/env python3
"""
Fix visibility issues across all pages.
The Webflow IX3 interaction engine sets initial hidden states (opacity:0, transforms)
on elements with animation attributes (fade-up, fade, text-anim, etc.).
In a static export, these initial states may get applied but the animations
may not fire properly, leaving elements invisible.

This script:
1. Adds a CSS override using a data attribute approach to force visibility, then
   removes the override before GSAP animates.
2. Replaces the old simple fade-up script with a comprehensive animation script.
3. Applies to all pages.
"""

import glob
import re

CSS_OVERRIDE = """
    <style>
      /* Safety-net visibility for Webflow IX3 animated elements.
         The .ix-ready class is added by our script AFTER it takes over animation control.
         Before .ix-ready, everything is forced visible so nothing stays hidden. */
      html:not(.ix-ready) [fade-up="true"],
      html:not(.ix-ready) [fade="true"],
      html:not(.ix-ready) [text-anim="true"],
      html:not(.ix-ready) [title-anim="true"],
      html:not(.ix-ready) [group-fade-up-item="true"],
      html:not(.ix-ready) [group-fade-up-parent="true"],
      html:not(.ix-ready) [scroll-to-text-color="true"],
      html:not(.ix-ready) [scroll-to-color-change="true"] {
        opacity: 1 !important;
        visibility: visible !important;
        transform: none !important;
      }
      /* Ensure section labels are always visible */
      .section-label-wrap,
      .section-label,
      .section-label-icon,
      .process-title-with-label,
      .team-title-with-label,
      .testimonial-section-details,
      .faq-section-details,
      .team-title-wrap,
      .faq-content-box,
      .process-section-top,
      .process-section-details-with-btn,
      .team-content-wrap,
      .team-grid,
      .testimonial-content-wrap,
      .testimonial-item-grid,
      .faq-item-wrap,
      .blog-content-wrap,
      .faq-more-question {
        opacity: 1 !important;
        visibility: visible !important;
      }
      /* Ensure the section label badges look correct */
      .section-label {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
      }
      .section-label-wrap {
        display: block !important;
      }
      /* Hide the Made in Webflow badge */
      .w-webflow-badge {
        display: none !important;
      }
    </style>
"""

ANIMATION_SCRIPT = """
    <script>
      /* Comprehensive Webflow IX3 animation replacement */
      document.addEventListener("DOMContentLoaded", () => {
        if (!window.gsap || !window.ScrollTrigger) return;
        gsap.registerPlugin(ScrollTrigger);

        /* Mark html as animation-ready, removing the CSS safety-net overrides.
           This lets GSAP control opacity/transform via inline styles. */
        document.documentElement.classList.add("ix-ready");

        /* Clear any IX3-applied inline styles on animated elements */
        document.querySelectorAll('[fade-up="true"], [fade="true"], [text-anim="true"]').forEach(el => {
          el.style.removeProperty('opacity');
          el.style.removeProperty('transform');
          el.style.removeProperty('visibility');
        });

        /* ---- FADE-UP elements ---- */
        gsap.utils.toArray('[fade-up="true"]').forEach((el) => {
          gsap.fromTo(el,
            { opacity: 0, y: 40 },
            {
              opacity: 1, y: 0,
              duration: 0.8,
              ease: "power3.out",
              scrollTrigger: {
                trigger: el,
                start: "top 90%",
                toggleActions: "play none none none"
              }
            }
          );
        });

        /* ---- FADE elements ---- */
        gsap.utils.toArray('[fade="true"]').forEach((el) => {
          gsap.fromTo(el,
            { opacity: 0 },
            {
              opacity: 1,
              duration: 1,
              ease: "power2.out",
              scrollTrigger: {
                trigger: el,
                start: "top 90%",
                toggleActions: "play none none none"
              }
            }
          );
        });

        /* ---- TEXT-ANIM elements ---- */
        gsap.utils.toArray('[text-anim="true"]').forEach((el) => {
          gsap.fromTo(el,
            { opacity: 0, y: 20 },
            {
              opacity: 1, y: 0,
              duration: 0.8,
              ease: "power2.out",
              scrollTrigger: {
                trigger: el,
                start: "top 90%",
                toggleActions: "play none none none"
              }
            }
          );
        });

        /* ---- Marquee slide animations ---- */
        gsap.utils.toArray('[marquee-slide-left="true"]').forEach((el) => {
          gsap.fromTo(el,
            { xPercent: 0 },
            {
              xPercent: -100,
              duration: 30,
              ease: "none",
              repeat: -1
            }
          );
        });

        gsap.utils.toArray('[marquee-slide-right="true"]').forEach((el) => {
          gsap.fromTo(el,
            { xPercent: -100 },
            {
              xPercent: 0,
              duration: 30,
              ease: "none",
              repeat: -1
            }
          );
        });
      });
    </script>
"""

files = glob.glob("**/*.html", recursive=True)

for f in files:
    if 'components/' in f or 'site-reference/' in f:
        continue

    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    changed = False

    # 1. Remove old CSS override if present (from previous run)
    old_css_pattern = r'<style>\s*/\* Force visibility for all Webflow IX3 animated elements.*?</style>'
    if re.search(old_css_pattern, content, re.DOTALL):
        content = re.sub(old_css_pattern, '', content, flags=re.DOTALL)
        changed = True

    # 2. Add new CSS override in <head> if not already present
    if 'Safety-net visibility for Webflow IX3 animated elements' not in content:
        content = content.replace('</head>', CSS_OVERRIDE + '\n  </head>')
        changed = True

    # 3. Remove old comprehensive animation script if present (from previous run)
    old_anim_pattern = r'<script>\s*/\* Comprehensive Webflow IX3 animation replacement \*/.*?</script>'
    if re.search(old_anim_pattern, content, re.DOTALL):
        content = re.sub(old_anim_pattern, '', content, flags=re.DOTALL)
        changed = True

    # 4. Remove the even older simple fade-up script if still present
    old_simple_pattern = r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*if \(!window\.gsap\) return;\s*gsap\.registerPlugin\(ScrollTrigger\);\s*gsap\.utils\.toArray\(\'\[fade-up="true"\]\'\)\.forEach.*?\}\);\s*\}\);\s*</script>'
    if re.search(old_simple_pattern, content, re.DOTALL):
        content = re.sub(old_simple_pattern, '', content, flags=re.DOTALL)
        changed = True

    # 5. Add comprehensive animation script before </body>
    if 'Comprehensive Webflow IX3 animation replacement' not in content:
        content = content.replace('</body>', ANIMATION_SCRIPT + '\n</body>')
        changed = True

    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated: {f}")

print("Done! All pages updated with visibility fixes and comprehensive animations.")
