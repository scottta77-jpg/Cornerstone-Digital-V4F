import json
import os
import re

def main():
    root_dir = "/Users/boyka777/Cornerstone Digital V4F/Cornerstone Digital V4F"
    pack_dir = "/Users/boyka777/Cornerstone Digital V4F/cornerstone-blog-pack"

    with open(os.path.join(pack_dir, "cms-content.json"), "r", encoding="utf-8") as f:
        articles = json.load(f)

    with open(os.path.join(pack_dir, "schema-blueprints.json"), "r", encoding="utf-8") as f:
        blueprints = json.load(f)

    bp_map = {bp["post_id"]: bp["schema"] for bp in blueprints}
    art_map = {art["id"]: art for art in articles}

    # Load template HTML from an existing blog detail page
    template_path = os.path.join(root_dir, "blog", "maximizing-conversion-with-strategic-web-design.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # Define CTA style to inject
    cta_and_custom_css = """
      /* Shared Yellow CTA Component */
      .cornerstone-blog-cta {
        margin-top: 2.5rem;
        margin-bottom: 2.5rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
      }
      .cornerstone-blog-cta p {
        margin-bottom: 1.5rem;
        font-size: 1.125rem;
        line-height: 1.6;
        color: #e5e5e7;
      }
      .cornerstone-blog-cta__button,
      .blog-details-body a.cornerstone-blog-cta__button,
      .blog-details-body .cornerstone-blog-cta a {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 48px;
        max-width: 100%;
        padding: 16px 24px !important;
        background: #f0e226 !important;
        color: #111112 !important;
        font-family: inherit;
        font-size: 0.875rem !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
        text-align: center;
        text-decoration: none !important;
        border: 2px solid #f0e226 !important;
        border-radius: 4px;
        box-sizing: border-box;
        transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
      }
      .cornerstone-blog-cta__button:hover,
      .blog-details-body a.cornerstone-blog-cta__button:hover,
      .blog-details-body .cornerstone-blog-cta a:hover {
        background: #f7c324 !important;
        border-color: #f7c324 !important;
        color: #111112 !important;
        text-decoration: none !important;
      }
      .cornerstone-blog-cta__button:focus-visible,
      .blog-details-body a.cornerstone-blog-cta__button:focus-visible,
      .blog-details-body .cornerstone-blog-cta a:focus-visible {
        outline: 3px solid #ffffff !important;
        outline-offset: 4px;
      }
      /* Rich text typography & table */
      .blog-details-body a:not(.cornerstone-blog-cta__button) {
        color: #f0e226;
        text-decoration: underline;
        text-underline-offset: 3px;
        transition: color 0.2s ease;
      }
      .blog-details-body a:not(.cornerstone-blog-cta__button):hover {
        color: #ffffff;
      }
      .blog-details-body table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.75rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
      }
      .blog-details-body th,
      .blog-details-body td {
        padding: 12px 16px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        text-align: left;
      }
      .blog-details-body th {
        background-color: rgba(240, 226, 38, 0.08);
        color: #f0e226;
        font-weight: 600;
      }
      .blog-details-body td {
        background-color: rgba(255, 255, 255, 0.02);
        color: #d1d1d6;
      }
      .blog-details-body tr:hover td {
        background-color: rgba(255, 255, 255, 0.04);
      }
      @media (max-width: 767px) {
        .blog-details-body table {
          display: block;
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
        }
      }
    """

    for art in articles:
        aid = art["id"]
        slug = art["slug"]
        asset = art["asset"]
        title = art["title"]
        seo_title = art["seo_title"]
        excerpt = art["excerpt"]
        meta_desc = art["meta_description"]
        category = art["category"]
        read_time = f"{art['read_time_minutes']} min"
        author = "Cornerstone Digital"
        thumb_web_path = f"/assets/images/blog/{asset}.webp"
        thumb_full_url = f"https://cornerstonedg.com/assets/images/blog/{asset}.webp"
        thumb_alt = art["thumbnail_alt"]
        canonical_url = art["proposed_url"]
        related_ids = art["related_post_ids"]

        # Parse body and extract the closing invitation paragraph
        body_html = art["content_html"].strip()

        # Find the last paragraph which contains the booking link
        # e.g.: <p>...<a href="https://cornerstonedg.com/#booking">...</a>...</p>
        paragraphs = re.findall(r'<p>.*?</p>', body_html, re.DOTALL)
        closing_copy_text = ""
        main_body_html = body_html

        if paragraphs:
            last_p = paragraphs[-1]
            if "https://cornerstonedg.com/#booking" in last_p:
                # Remove link tags inside this paragraph to leave clean text
                closing_copy_text = re.sub(r'</?a[^>]*>', '', last_p)
                # Remove outer <p>...</p> tags
                closing_copy_text = re.sub(r'^<p>\s*|\s*</p>$', '', closing_copy_text)
                # Remove this last paragraph from the main body HTML
                # Find last occurrence of last_p and remove it
                idx = main_body_html.rfind(last_p)
                if idx != -1:
                    main_body_html = main_body_html[:idx].rstrip()

        # Build the CTA HTML
        cta_html = f"""<div class="cornerstone-blog-cta">
<p class="text-regular">{closing_copy_text}</p>
<a class="cornerstone-blog-cta__button" style="color: #111112 !important; text-decoration: none !important;" href="https://cornerstonedg.com/#booking">
  BOOK YOUR 15-MINUTE DISCOVERY CALL <span aria-hidden="true">→</span>
</a>
</div>"""

        full_richtext = main_body_html + "\n" + cta_html

        # Generate JSON-LD Schema
        schema_dict = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": meta_desc,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical_url
            },
            "author": {
                "@type": "Organization",
                "name": "Cornerstone Digital",
                "url": "https://cornerstonedg.com/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Cornerstone Digital",
                "url": "https://cornerstonedg.com/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://cornerstonedg.com/assets/images/cornerstone-logo-3.webp"
                }
            },
            "image": thumb_full_url,
            "datePublished": "2026-10-21T12:00:00+01:00",
            "dateModified": "2026-10-21T12:00:00+01:00",
            "inLanguage": "en-GB",
            "articleSection": category,
            "wordCount": art["word_count"]
        }
        json_ld_str = json.dumps(schema_dict, indent=2, ensure_ascii=False)

        # Build related articles HTML (take first 2 related articles)
        rel_cards_html = []
        for rid in related_ids[:2]:
            rel_art = art_map.get(rid)
            if not rel_art:
                continue
            r_slug = rel_art["slug"]
            r_title = rel_art["title"]
            r_excerpt = rel_art["excerpt"]
            r_thumb = f"/assets/images/blog/{rel_art['asset']}.webp"

            card = f"""<div fade-up="true" role="listitem" class="w-dyn-item"><a href="/blog/{r_slug}" class="blog-item w-inline-block"><div move-over-parent="true" class="blog-item-banner-wrap"><img loading="lazy" src="{r_thumb}" alt="" width="1672" height="941" sizes="(max-width: 767px) 100vw, (max-width: 991px) 727px, 939px" class="cover-size-image"/><div move-over-item="true" class="item-view-btn-wrap"><div class="item-view-btn">View<br/>Details</div></div></div><div class="blog-item-title-with-para"><h3 class="h4">{r_title}</h3><p class="text-regular">{r_excerpt}</p></div></a></div>"""
            rel_cards_html.append(card)

        all_rel_html = "".join(rel_cards_html)

        # Start assembling the page from template_html
        page_html = template_html

        # 1. Update <title>
        page_title = f"{seo_title} | Cornerstone Digital"
        page_html = re.sub(r'<title>.*?</title>', f'<title>{page_title}</title>', page_html, flags=re.DOTALL)

        # 2. Update canonical & meta description
        page_html = re.sub(r'<meta content=".*?" name="description"/>', f'<meta content="{meta_desc}" name="description"/>', page_html)
        if '<link rel="canonical"' in page_html:
            page_html = re.sub(r'<link rel="canonical".*?/>', f'<link rel="canonical" href="{canonical_url}"/>', page_html)
        else:
            page_html = page_html.replace('</head>', f'<link rel="canonical" href="{canonical_url}"/>\n</head>')

        # 3. Update OG / Twitter metadata
        page_html = re.sub(r'<meta content=".*?" property="og:title"/>', f'<meta content="{seo_title}" property="og:title"/>', page_html)
        page_html = re.sub(r'<meta content=".*?" property="og:description"/>', f'<meta content="{meta_desc}" property="og:description"/>', page_html)
        page_html = re.sub(r'<meta content=".*?" property="og:image"/>', f'<meta content="{thumb_full_url}" property="og:image"/>', page_html)

        page_html = re.sub(r'<meta content=".*?" name="twitter:title"/>', f'<meta content="{seo_title}" name="twitter:title"/>', page_html)
        page_html = re.sub(r'<meta content=".*?" name="twitter:description"/>', f'<meta content="{meta_desc}" name="twitter:description"/>', page_html)
        page_html = re.sub(r'<meta content=".*?" name="twitter:image"/>', f'<meta content="{thumb_full_url}" name="twitter:image"/>', page_html)

        # Add og:url if not present
        if 'property="og:url"' in page_html:
            page_html = re.sub(r'<meta content=".*?" property="og:url"/>', f'<meta content="{canonical_url}" property="og:url"/>', page_html)
        else:
            page_html = page_html.replace('<meta property="og:type"', f'<meta property="og:url" content="{canonical_url}"/><meta property="og:type"')

        # 4. Replace JSON-LD script
        json_ld_tag = f'<script type="application/ld+json">\n{json_ld_str}\n</script>'
        page_html = re.sub(r'<script type="application/ld\+json">.*?</script>', json_ld_tag, page_html, flags=re.DOTALL)

        # 5. Inject CTA and custom styles into <head>
        if '.cornerstone-blog-cta' not in page_html:
            page_html = page_html.replace('</style>', f'{cta_and_custom_css}\n</style>')

        # 6. Replace Left Sidebar: Thumbnail image, Subject, Read Time, Author
        # Thumbnail image:
        old_banner_regex = r'<div group-fade-up-item="true" class="blog-details-banner-wrap"><img src="[^"]*"[^>]*class="cover-size-image"/></div>'
        new_banner = f'<div group-fade-up-item="true" class="blog-details-banner-wrap"><img src="{thumb_web_path}" loading="lazy" alt="{thumb_alt}" width="1672" height="941" sizes="(max-width: 767px) 100vw, (max-width: 991px) 727px, 939px" class="cover-size-image"/></div>'
        page_html = re.sub(old_banner_regex, new_banner, page_html)

        # Key-with-value items:
        # Subject:
        page_html = re.sub(
            r'(<div class="h6">Subject</div></div><div class="h6">)[^<]*(</div>)',
            rf'\g<1>{category}\g<2>',
            page_html
        )
        # Read Time:
        page_html = re.sub(
            r'(<div class="h6">Read Time</div></div><div class="h6">)[^<]*(</div>)',
            rf'\g<1>{read_time}\g<2>',
            page_html
        )
        # Author:
        page_html = re.sub(
            r'(<div class="h6">Author</div></div><div class="h6">)[^<]*(</div>)',
            rf'\g<1>{author}\g<2>',
            page_html
        )

        # 7. Replace Right Column: H1, Excerpt, Body
        # H1:
        page_html = re.sub(
            r'<h1 group-fade-up-item="true" class="h1">.*?</h1>',
            f'<h1 group-fade-up-item="true" class="h1">{title}</h1>',
            page_html,
            flags=re.DOTALL
        )
        # Excerpt:
        page_html = re.sub(
            r'<p group-fade-up-item="true" class="text-regular">.*?</p>',
            f'<p group-fade-up-item="true" class="text-regular">{excerpt}</p>',
            page_html,
            count=1,
            flags=re.DOTALL
        )
        # Body:
        old_body_regex = r'<div group-fade-up-item="true" class="blog-details-body w-richtext">.*?</div></div></div></div></section>'
        new_body = f'<div group-fade-up-item="true" class="blog-details-body w-richtext">{full_richtext}</div></div></div></div></section>'
        page_html = re.sub(old_body_regex, new_body, page_html, flags=re.DOTALL)

        # 8. Related Articles Section:
        # Section label text -> "Articles"
        page_html = re.sub(
            r'(<div class="text-block">\s*)FAQ(\s*</div>)',
            r'\g<1>Articles\g<2>',
            page_html
        )
        page_html = re.sub(
            r'<div class="h1">Questions</div>',
            r'<div class="h1">Articles</div>',
            page_html
        )
        page_html = re.sub(
            r'<p fade-up="true" class="text-regular home-blog-para">.*?</p>',
            r'<p fade-up="true" class="text-regular home-blog-para">Explore more practical guides to improve your website, visibility and conversions.</p>',
            page_html
        )

        # Related items cards
        old_rel_list_regex = r'<div class="w-dyn-list"><div role="list" class="blog-collection-list w-dyn-items">.*?</div></div></div></div></section>'
        new_rel_list = f'<div class="w-dyn-list"><div role="list" class="blog-collection-list w-dyn-items">{all_rel_html}</div></div></div></div></section>'
        page_html = re.sub(old_rel_list_regex, new_rel_list, page_html, flags=re.DOTALL)

        # Clean leftover Olyyx references in business branding
        page_html = page_html.replace('data-wf-item-slug="maximizing-conversion-with-strategic-web-design"', f'data-wf-item-slug="{slug}"')
        page_html = page_html.replace('data-wf-item-slug="minimalist-branding-for-modern-tech-startups"', f'data-wf-item-slug="{slug}"')
        page_html = page_html.replace('data-wf-domain="olyyx.webflow.io"', 'data-wf-domain="cornerstonedg.com"')

        # Write to blog/<slug>.html and blog/<slug>/index.html
        target_file_html = os.path.join(root_dir, "blog", f"{slug}.html")
        target_dir = os.path.join(root_dir, "blog", slug)
        os.makedirs(target_dir, exist_ok=True)
        target_file_index = os.path.join(target_dir, "index.html")

        with open(target_file_html, "w", encoding="utf-8") as out:
            out.write(page_html)
        with open(target_file_index, "w", encoding="utf-8") as out:
            out.write(page_html)

        print(f"Generated post {aid}: {slug} -> {target_file_html} and {target_file_index}")

    # Also handle the alias 'why-your-website-isnt-generating-enquiries'
    p01_html = os.path.join(root_dir, "blog", "website-not-generating-enquiries.html")
    with open(p01_html, "r", encoding="utf-8") as f:
        p01_content = f.read()

    alias_dir = os.path.join(root_dir, "blog", "why-your-website-isnt-generating-enquiries")
    os.makedirs(alias_dir, exist_ok=True)
    with open(os.path.join(root_dir, "blog", "why-your-website-isnt-generating-enquiries.html"), "w", encoding="utf-8") as f:
        f.write(p01_content)
    with open(os.path.join(alias_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(p01_content)
    print("Generated alias why-your-website-isnt-generating-enquiries")

if __name__ == "__main__":
    main()
