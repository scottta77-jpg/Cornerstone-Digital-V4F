# Antigravity implementation prompt

Add the ten new Cornerstone Digital articles in this folder to the existing website and implement one scheduled release every Monday for ten consecutive weeks, starting 26 October 2026 and ending 28 December 2026.

Read `README.md`, `01-publishing-calendar.md`, `04-scheduling-and-technical-checklist.md`, `cms-content.json` and `publishing-schedule.json` first. Use the individual article files, matching WebP thumbnails, schema blueprints and shared CTA component. The review HTML is a reading reference; preserve the existing website's design and CMS structure.

Keep the earlier nine articles intact. These are posts 10–19 and must be added as new content. Use the supplied titles, bodies, excerpts, categories, reading times, organisation byline, SEO metadata, slugs and images. Keep source links and clearly labelled illustrative examples. Map contextual links to the actual existing routes; the earlier nine are listed in `existing-post-reference.json`.

Follow the exact Monday-to-article mapping in `publishing-schedule.json`. Use 09:00 Europe/London as the proposed default publishing hour and keep it configurable. Implement real automatic publication using the current CMS's native scheduler where available. If this is a static site, use an appropriate timed build/deployment or server-controlled release process through its existing hosting workflow. A JSON date, build-time filter with no rebuild, or client-side card hiding is not a working publishing schedule.

Keep future posts out of public routes, listing, featured content, related links, sitemap and feeds until their due time. Publish one new article on each assigned Monday, safely handling repeated job runs without duplicates. The series ends after post 19 on 28 December. Surface missed or overdue releases rather than silently publishing a backlog together.

Use accurate BlogPosting JSON-LD with the real publication/modification dates, author and publisher, canonical URL and final image URL. Consolidate any existing Article markup and keep visible metadata consistent. Do not add FAQ rich-result promises, invented people or unsupported outcomes.

Render the closing CTA already present in each article as the shared yellow button, once per article, after the final content section. Use the label `BOOK YOUR 15-MINUTE DISCOVERY CALL →` and the target `https://cornerstonedg.com/#booking`. Preserve the current dark/yellow design, accessible focus and mobile layout. Check leftover Olyyx branding while preserving licence-required credits.

Verify the publication boundaries, all ten planned releases, future-page visibility, routes, links, images, schema, metadata, sitemap/feed behaviour and mobile layouts. Run the project's relevant build checks. Complete everything supported by the available project access.

Finish with a concise implementation report stating what was added, the real scheduling mechanism, timezone, next and final release, validation completed and whether automatic publication is active. If activation needs missing credentials or configuration, identify the precise blocker; do not claim the posts are scheduled until the publishing system confirms it.
