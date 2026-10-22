#!/usr/bin/env python3
"""
Cornerstone Digital — Scheduled Blog Publisher
Authoritative scheduler and static page generator for the Cornerstone Digital website.

Usage:
    python3 publish_scheduled_posts.py                  # Evaluates current London time
    python3 publish_scheduled_posts.py --status         # Shows status table of all 19 posts
    python3 publish_scheduled_posts.py --now "2026-10-26T09:00:00+00:00"  # Simulates target timestamp
    python3 publish_scheduled_posts.py --reset          # Resets state to baseline (posts 01-09 published)
    python3 publish_scheduled_posts.py --publish-all    # Publishes all posts (for testing/preview)
"""

import argparse
import datetime
import json
import os
import re
import shutil
import sys
from zoneinfo import ZoneInfo

# Project directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACK_9_DIR = os.path.join(SCRIPT_DIR, "cornerstone-blog-pack")
PACK_10_DIR = os.path.join(SCRIPT_DIR, "cornerstone-weekly-blog-pack")
STATE_FILE = os.path.join(SCRIPT_DIR, "publishing-state.json")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "blog", "website-not-generating-enquiries.html")
SITEMAP_PATH = os.path.join(SCRIPT_DIR, "sitemap.xml")
LISTING_PATHS = [
    os.path.join(SCRIPT_DIR, "blogs", "index.html"),
    os.path.join(SCRIPT_DIR, "blog.html"),
    os.path.join(SCRIPT_DIR, "blog", "index.html"),
]

TIMEZONE_STR = "Europe/London"
LONDON_TZ = ZoneInfo(TIMEZONE_STR)

# Baseline static routes for sitemap
STATIC_PAGES = [
    {"loc": "https://cornerstonedg.com/", "priority": "1.0"},
    {"loc": "https://cornerstonedg.com/about/", "priority": "0.8"},
    {"loc": "https://cornerstonedg.com/services/", "priority": "0.8"},
    {"loc": "https://cornerstonedg.com/projects/", "priority": "0.8"},
    {"loc": "https://cornerstonedg.com/project/ecosphere/", "priority": "0.64"},
    {"loc": "https://cornerstonedg.com/contact/", "priority": "0.8"},
    {"loc": "https://cornerstonedg.com/blogs/", "priority": "0.8", "is_blogs_index": True},
]

LEGAL_PAGES = [
    {"loc": "https://cornerstonedg.com/privacy-policy/", "priority": "0.5"},
    {"loc": "https://cornerstonedg.com/terms-and-conditions/", "priority": "0.5"},
]


def load_all_article_definitions():
    """Load and merge articles and schema blueprints from both packs."""
    with open(os.path.join(PACK_9_DIR, "cms-content.json"), "r", encoding="utf-8") as f:
        pack9_articles = json.load(f)
    with open(os.path.join(PACK_9_DIR, "schema-blueprints.json"), "r", encoding="utf-8") as f:
        pack9_blueprints = json.load(f)

    with open(os.path.join(PACK_10_DIR, "cms-content.json"), "r", encoding="utf-8") as f:
        pack10_articles = json.load(f)
    with open(os.path.join(PACK_10_DIR, "schema-blueprints.json"), "r", encoding="utf-8") as f:
        pack10_blueprints = json.load(f)

    with open(os.path.join(PACK_10_DIR, "publishing-schedule.json"), "r", encoding="utf-8") as f:
        weekly_schedule = json.load(f)

    bp_map = {}
    for bp in pack9_blueprints:
        bp_map[bp["post_id"]] = bp["schema"]
    for bp in pack10_blueprints:
        bp_map[bp["post_id"]] = bp["schema"]

    schedule_map = {}
    for entry in weekly_schedule["posts"]:
        schedule_map[entry["post_id"]] = entry["planned_publish_at"]

    articles = []
    # 01-09
    for art in pack9_articles:
        art_id = art["id"]
        articles.append({
            "id": art_id,
            "title": art["title"],
            "seo_title": art["seo_title"],
            "slug": art["slug"],
            "proposed_url": art["proposed_url"],
            "category": art["category"],
            "pillar": art.get("pillar", ""),
            "excerpt": art["excerpt"],
            "meta_description": art["meta_description"],
            "author_name": "Cornerstone Digital",
            "author_type": "Organization",
            "asset": art["asset"],
            "thumbnail_alt": art.get("thumbnail_alt", ""),
            "related_post_ids": art.get("related_post_ids", []),
            "word_count": art.get("word_count", 700),
            "read_time_minutes": art.get("read_time_minutes", 4),
            "content_html": art["content_html"],
            "schema_blueprint": bp_map.get(art_id, {}),
            "planned_publish_at": "2026-10-21T12:00:00+01:00",
            "is_weekly_pack": False,
        })

    # 10-19
    for art in pack10_articles:
        art_id = art["id"]
        planned_time = schedule_map.get(art_id, art.get("planned_publish_at"))
        articles.append({
            "id": art_id,
            "title": art["title"],
            "seo_title": art["seo_title"],
            "slug": art["slug"],
            "proposed_url": art["proposed_url"],
            "category": art["category"],
            "pillar": art.get("pillar", ""),
            "excerpt": art["excerpt"],
            "meta_description": art["meta_description"],
            "author_name": "Cornerstone Digital",
            "author_type": "Organization",
            "asset": art["asset"],
            "thumbnail_alt": art.get("thumbnail_alt", ""),
            "related_post_ids": art.get("related_post_ids", []),
            "word_count": art.get("word_count", 700),
            "read_time_minutes": art.get("read_time_minutes", 4),
            "content_html": art["content_html"],
            "schema_blueprint": bp_map.get(art_id, {}),
            "planned_publish_at": planned_time,
            "is_weekly_pack": True,
        })

    return articles


def get_or_create_state(articles):
    """Load existing publication state or initialize baseline."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            return state
        except Exception as e:
            print(f"[Warning] Failed to read {STATE_FILE}: {e}. Reinitializing.")

    # Initialize baseline
    state = {
        "site": "https://cornerstonedg.com/",
        "timezone": TIMEZONE_STR,
        "default_publish_time": "09:00:00",
        "last_run_at": None,
        "articles": {}
    }

    for art in articles:
        art_id = art["id"]
        if int(art_id) <= 9:
            # Baseline 9 posts published on Oct 21, 2026
            state["articles"][art_id] = {
                "id": art_id,
                "slug": art["slug"],
                "status": "published",
                "planned_publish_at": art["planned_publish_at"],
                "published_at": art["planned_publish_at"],
            }
        else:
            state["articles"][art_id] = {
                "id": art_id,
                "slug": art["slug"],
                "status": "scheduled",
                "planned_publish_at": art["planned_publish_at"],
                "published_at": None,
            }

    save_state(state)
    return state


def save_state(state):
    """Atomically save publication state."""
    state["last_run_at"] = datetime.datetime.now(LONDON_TZ).isoformat()
    tmp_file = STATE_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp_file, STATE_FILE)


def parse_iso(dt_str):
    """Parse an ISO 8601 timestamp into a timezone-aware datetime."""
    dt = datetime.datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LONDON_TZ)
    return dt


def ensure_thumbnail_copied(asset):
    """Ensure the article thumbnail WebP and PNG exist in assets/images/blog/."""
    dest_dir = os.path.join(SCRIPT_DIR, "assets", "images", "blog")
    os.makedirs(dest_dir, exist_ok=True)
    webp_name = f"{asset}.webp"
    png_name = f"{asset}.png"

    dest_webp = os.path.join(dest_dir, webp_name)
    if not os.path.exists(dest_webp):
        # Look in pack 10 thumbnails first, then pack 9
        for src_pack in [PACK_10_DIR, PACK_9_DIR]:
            src_webp = os.path.join(src_pack, "thumbnails", webp_name)
            if os.path.exists(src_webp):
                shutil.copy2(src_webp, dest_webp)
                break

    dest_png = os.path.join(dest_dir, png_name)
    if not os.path.exists(dest_png):
        for src_pack in [PACK_10_DIR, PACK_9_DIR]:
            src_png = os.path.join(src_pack, "thumbnails", png_name)
            if os.path.exists(src_png):
                shutil.copy2(src_png, dest_png)
                break


def build_article_html(art, published_at, published_articles_map, template_html):
    """Generate the full HTML for an individual article."""
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
    canonical_url = f"https://cornerstonedg.com/blog/{slug}/"

    ensure_thumbnail_copied(asset)

    # Closing CTA verification:
    body_html = art["content_html"].strip()
    cta_marker = 'class="cornerstone-blog-cta"'
    if cta_marker not in body_html:
        body_html += (
            '\n<div class="cornerstone-blog-cta">'
            '<a class="cornerstone-blog-cta__button" href="https://cornerstonedg.com/#booking">'
            'BOOK YOUR 15-MINUTE DISCOVERY CALL <span aria-hidden="true">→</span></a></div>'
        )

    # JSON-LD Schema
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
        "datePublished": published_at,
        "dateModified": published_at,
        "inLanguage": "en-GB",
        "articleSection": category,
        "wordCount": art["word_count"]
    }
    json_ld_str = json.dumps(schema_dict, indent=2, ensure_ascii=False)

    # Related Articles: only include those that are currently published
    rel_cards_html = []
    for rid in art.get("related_post_ids", []):
        rel_art = published_articles_map.get(rid)
        if not rel_art:
            continue
        r_slug = rel_art["slug"]
        r_title = rel_art["title"]
        r_excerpt = rel_art["excerpt"]
        r_thumb = f"/assets/images/blog/{rel_art['asset']}.webp"

        card = (
            f'<div fade-up="true" role="listitem" class="w-dyn-item">'
            f'<a href="/blog/{r_slug}" class="blog-item w-inline-block">'
            f'<div move-over-parent="true" class="blog-item-banner-wrap">'
            f'<img loading="lazy" src="{r_thumb}" alt="" width="1672" height="941" sizes="(max-width: 767px) 100vw, (max-width: 991px) 727px, 939px" class="cover-size-image"/>'
            f'<div move-over-item="true" class="item-view-btn-wrap"><div class="item-view-btn">View<br/>Details</div></div>'
            f'</div>'
            f'<div class="blog-item-title-with-para"><h3 class="h4">{r_title}</h3><p class="text-regular">{r_excerpt}</p></div>'
            f'</a></div>'
        )
        rel_cards_html.append(card)
        if len(rel_cards_html) == 2:
            break

    all_rel_html = "".join(rel_cards_html)

    page_html = template_html

    # 1. Title
    page_title = f"{seo_title} | Cornerstone Digital"
    page_html = re.sub(r'<title>.*?</title>', f'<title>{page_title}</title>', page_html, flags=re.DOTALL)

    # 2. Canonical & description
    page_html = re.sub(r'<meta\s+[^>]*?name="description"[^>]*?>', f'<meta name="description" content="{meta_desc}"/>', page_html)
    if '<link rel="canonical"' in page_html:
        page_html = re.sub(r'<link rel="canonical".*?/>', f'<link rel="canonical" href="{canonical_url}"/>', page_html)
    else:
        page_html = page_html.replace('</head>', f'<link rel="canonical" href="{canonical_url}"/>\n</head>')

    # 3. OG / Twitter metadata
    page_html = re.sub(r'<meta\s+[^>]*?property="og:title"[^>]*?>', f'<meta property="og:title" content="{seo_title}"/>', page_html)
    page_html = re.sub(r'<meta\s+[^>]*?property="og:description"[^>]*?>', f'<meta property="og:description" content="{meta_desc}"/>', page_html)
    page_html = re.sub(r'<meta\s+[^>]*?property="og:image"[^>]*?>', f'<meta property="og:image" content="{thumb_full_url}"/>', page_html)
    page_html = re.sub(r'<meta\s+[^>]*?property="og:url"[^>]*?>', f'<meta property="og:url" content="{canonical_url}"/>', page_html)

    page_html = re.sub(r'<meta\s+[^>]*?name="twitter:title"[^>]*?>', f'<meta name="twitter:title" content="{seo_title}"/>', page_html)
    page_html = re.sub(r'<meta\s+[^>]*?name="twitter:description"[^>]*?>', f'<meta name="twitter:description" content="{meta_desc}"/>', page_html)
    page_html = re.sub(r'<meta\s+[^>]*?name="twitter:image"[^>]*?>', f'<meta name="twitter:image" content="{thumb_full_url}"/>', page_html)

    # 4. JSON-LD script
    json_ld_tag = f'<script type="application/ld+json">\n{json_ld_str}\n</script>'
    page_html = re.sub(r'<script type="application/ld\+json">.*?</script>', json_ld_tag, page_html, flags=re.DOTALL)

    # 5. Sidebar: Thumbnail image, Subject, Read Time, Author
    old_banner_regex = r'<div group-fade-up-item="true" class="blog-details-banner-wrap"><img src="[^"]*"[^>]*class="cover-size-image"/></div>'
    new_banner = f'<div group-fade-up-item="true" class="blog-details-banner-wrap"><img src="{thumb_web_path}" loading="lazy" alt="{thumb_alt}" width="1672" height="941" sizes="(max-width: 767px) 100vw, (max-width: 991px) 727px, 939px" class="cover-size-image"/></div>'
    page_html = re.sub(old_banner_regex, new_banner, page_html)

    page_html = re.sub(r'(<div class="h6">Subject</div></div><div class="h6">)[^<]*(</div>)', rf'\g<1>{category}\g<2>', page_html)
    page_html = re.sub(r'(<div class="h6">Read Time</div></div><div class="h6">)[^<]*(</div>)', rf'\g<1>{read_time}\g<2>', page_html)
    page_html = re.sub(r'(<div class="h6">Author</div></div><div class="h6">)[^<]*(</div>)', rf'\g<1>{author}\g<2>', page_html)

    # 6. Right Column: H1, Excerpt, Body
    page_html = re.sub(r'<h1 group-fade-up-item="true" class="h1">.*?</h1>', f'<h1 group-fade-up-item="true" class="h1">{title}</h1>', page_html, flags=re.DOTALL)
    page_html = re.sub(r'<p group-fade-up-item="true" class="text-regular">.*?</p>', f'<p group-fade-up-item="true" class="text-regular">{excerpt}</p>', page_html, count=1, flags=re.DOTALL)

    old_body_regex = r'<div group-fade-up-item="true" class="blog-details-body w-richtext">.*?</div></div></div></div></section>'
    new_body = f'<div group-fade-up-item="true" class="blog-details-body w-richtext">{body_html}</div></div></div></div></section>'
    page_html = re.sub(old_body_regex, new_body, page_html, flags=re.DOTALL)

    # 7. Related Articles Section
    old_rel_list_regex = r'<div class="w-dyn-list"><div role="list" class="blog-collection-list w-dyn-items">.*?</div></div></div></div></section>'
    new_rel_list = f'<div class="w-dyn-list"><div role="list" class="blog-collection-list w-dyn-items">{all_rel_html}</div></div></div></div></section>'
    page_html = re.sub(old_rel_list_regex, new_rel_list, page_html, flags=re.DOTALL)

    # Clean legacy branding
    page_html = page_html.replace('data-wf-domain="olyyx.webflow.io"', 'data-wf-domain="cornerstonedg.com"')
    page_html = re.sub(r'data-wf-item-slug="[^"]*"', f'data-wf-item-slug="{slug}"', page_html)

    return page_html


def write_article_files(art, page_html):
    """Write both /blog/<slug>.html and /blog/<slug>/index.html."""
    slug = art["slug"]
    blog_dir = os.path.join(SCRIPT_DIR, "blog")
    os.makedirs(blog_dir, exist_ok=True)

    file_html = os.path.join(blog_dir, f"{slug}.html")
    dir_slug = os.path.join(blog_dir, slug)
    os.makedirs(dir_slug, exist_ok=True)
    file_index = os.path.join(dir_slug, "index.html")

    with open(file_html, "w", encoding="utf-8") as f:
        f.write(page_html)
    with open(file_index, "w", encoding="utf-8") as f:
        f.write(page_html)

    # Special alias for post 01
    if art["id"] == "01":
        alias_file = os.path.join(blog_dir, "why-your-website-isnt-generating-enquiries.html")
        alias_dir = os.path.join(blog_dir, "why-your-website-isnt-generating-enquiries")
        os.makedirs(alias_dir, exist_ok=True)
        with open(alias_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        with open(os.path.join(alias_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html)


def remove_unpublished_article_files(art):
    """Ensure an unpublished post does not exist on disk in public routes."""
    slug = art["slug"]
    blog_dir = os.path.join(SCRIPT_DIR, "blog")
    file_html = os.path.join(blog_dir, f"{slug}.html")
    dir_slug = os.path.join(blog_dir, slug)

    if os.path.exists(file_html):
        try:
            os.remove(file_html)
        except Exception:
            pass
    if os.path.exists(dir_slug):
        try:
            shutil.rmtree(dir_slug)
        except Exception:
            pass


def update_blog_listings(published_articles):
    """Update blogs/index.html, blog.html, and blog/index.html with published posts."""
    # Featured Hero is Post 01
    art_map = {a["id"]: a for a in published_articles}
    p01 = art_map.get("01")
    if not p01:
        return

    # Cards are all other published articles sorted newest to oldest
    # Posts with id > 9 sorted descending, then 09 down to 02
    weekly_published = [a for a in published_articles if int(a["id"]) >= 10]
    weekly_published.sort(key=lambda x: x["planned_publish_at"], reverse=True)

    base_published = [a for a in published_articles if 2 <= int(a["id"]) <= 9]
    base_published.sort(key=lambda x: int(x["id"])) # 02 through 09

    # Combine: newest weekly at top, followed by 02-09
    card_posts = weekly_published + base_published

    # Read base listing
    listing_path = LISTING_PATHS[0]
    with open(listing_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Meta
    html = re.sub(r'<title>.*?</title>', '<title>Blogs | Cornerstone Digital</title>', html)
    html = re.sub(
        r'<meta content=".*?" name="description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." name="description"/>',
        html
    )
    html = re.sub(r'<meta content=".*?" property="og:title"/>', '<meta content="Blogs | Cornerstone Digital" property="og:title"/>', html)
    html = re.sub(
        r'<meta content=".*?" property="og:description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." property="og:description"/>',
        html
    )
    html = re.sub(r'<meta content=".*?" property="og:image"/>', '<meta content="https://cornerstonedg.com/assets/images/blog/01-website-enquiries.webp" property="og:image"/>', html)
    html = re.sub(r'<meta content=".*?" name="twitter:title"/>', '<meta content="Blogs | Cornerstone Digital" name="twitter:title"/>', html)
    html = re.sub(
        r'<meta content=".*?" name="twitter:description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." name="twitter:description"/>',
        html
    )
    html = re.sub(r'<meta content=".*?" name="twitter:image"/>', '<meta content="https://cornerstonedg.com/assets/images/blog/01-website-enquiries.webp" name="twitter:image"/>', html)

    # Collection Schema
    item_list_elements = []
    # Include hero post first in schema
    all_published_ordered = [p01] + card_posts
    for idx, art in enumerate(all_published_ordered, 1):
        item_list_elements.append({
            "@type": "BlogPosting",
            "position": idx,
            "headline": art["title"],
            "description": art["meta_description"],
            "url": f"https://cornerstonedg.com/blog/{art['slug']}/",
            "image": f"https://cornerstonedg.com/assets/images/blog/{art['asset']}.webp"
        })

    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Cornerstone Digital Blog",
        "description": "Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses.",
        "url": "https://cornerstonedg.com/blogs/",
        "publisher": {
            "@type": "Organization",
            "name": "Cornerstone Digital",
            "url": "https://cornerstonedg.com/"
        },
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": item_list_elements
        }
    }
    new_json_ld = f'<script type="application/ld+json">\n{json.dumps(collection_schema, indent=2, ensure_ascii=False)}\n</script>'
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', new_json_ld, html, flags=re.DOTALL)

    # Generate card markup
    cards_html_list = []
    for art in card_posts:
        slug = art["slug"]
        asset = art["asset"]
        title = art["title"]
        excerpt = art["excerpt"]
        thumb = f"/assets/images/blog/{asset}.webp"

        card = f"""<div class="w-dyn-item" fade-up="true" role="listitem">
<a class="blog-item w-inline-block" href="/blog/{slug}"> <div class="blog-item-banner-wrap" move-over-parent="true">
<img alt="" class="cover-size-image" loading="lazy" width="1672" height="941" sizes="(max-width: 767px) 100vw, (max-width: 991px) 727px, 940px" src="{thumb}"/>
<div class="item-view-btn-wrap" move-over-item="true">
<div class="item-view-btn">
                      View
                      <br/>
                      Details
                    </div>
</div>
</div>
<div class="blog-item-title-with-para">
<h3 class="h4">
                    {title}
                  </h3>
<p class="text-regular">
                    {excerpt}
                  </p>
</div>
</a>
</div>"""
        cards_html_list.append(card)

    all_cards_html = "\n".join(cards_html_list)

    # Replace collection list content
    cards_regex = r'<div class="blog-collection-list w-dyn-items" role="list">.*?</div>'
    new_cards_wrapper = f'<div class="blog-collection-list w-dyn-items" role="list">\n{all_cards_html}\n</div>'
    html = re.sub(cards_regex, new_cards_wrapper, html, flags=re.DOTALL)

    for p in LISTING_PATHS:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)


def update_sitemap(published_articles):
    """Generate accurate sitemap.xml containing only published URLs."""
    today_str = datetime.datetime.now(LONDON_TZ).strftime("%Y-%m-%d")

    urls = []
    # Static pages
    for page in STATIC_PAGES:
        entry = f"""  <url>
    <loc>{page['loc']}</loc>
    <priority>{page['priority']}</priority>"""
        if page.get("is_blogs_index"):
            entry += f"\n    <lastmod>{today_str}</lastmod>"
        entry += "\n  </url>"
        urls.append(entry)

    # Published articles
    for art in published_articles:
        slug = art["slug"]
        pub_at = art.get("published_at") or art.get("planned_publish_at")
        pub_date = pub_at[:10] if pub_at else today_str
        entry = f"""  <url>
    <loc>https://cornerstonedg.com/blog/{slug}/</loc>
    <lastmod>{pub_date}</lastmod>
    <priority>0.7</priority>
  </url>"""
        urls.append(entry)

    # Legal pages
    for page in LEGAL_PAGES:
        urls.append(f"""  <url>
    <loc>{page['loc']}</loc>
    <priority>{page['priority']}</priority>
  </url>""")

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_content += "\n".join(urls)
    sitemap_content += "\n</urlset>\n"

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_content)


def run_publisher(target_time=None, dry_run=False, publish_all=False, reset=False):
    """Main publishing coordinator."""
    articles = load_all_article_definitions()

    if reset:
        print("[Reset] Resetting state and disk to baseline (posts 01-09 published).")
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        state = get_or_create_state(articles)
        # Remove any weekly posts on disk
        for art in articles:
            if art["is_weekly_pack"]:
                remove_unpublished_article_files(art)
        # Update listing and sitemap with only 01-09
        base_published = [a for a in articles if int(a["id"]) <= 9]
        update_blog_listings(base_published)
        update_sitemap(base_published)
        print("[Reset] Done.")
        return

    state = get_or_create_state(articles)

    if target_time is None:
        target_time = datetime.datetime.now(LONDON_TZ)
    elif isinstance(target_time, str):
        target_time = parse_iso(target_time)

    print(f"[Scheduler] Evaluating against: {target_time.isoformat()} ({TIMEZONE_STR})")

    # Determine which articles should be published
    published_arts = []
    newly_published = []

    # Map of all articles by ID for easy lookup
    art_by_id = {a["id"]: a for a in articles}

    # First pass: identify newly due posts
    for art in articles:
        aid = art["id"]
        st = state["articles"].get(aid, {})
        current_status = st.get("status", "scheduled")
        planned_dt = parse_iso(art["planned_publish_at"])

        if publish_all:
            should_publish = True
        elif current_status == "published":
            should_publish = True
        else:
            should_publish = planned_dt <= target_time

        if should_publish:
            pub_at = st.get("published_at") or art["planned_publish_at"]
            if current_status != "published":
                newly_published.append(art)
                st["status"] = "published"
                st["published_at"] = pub_at
                state["articles"][aid] = st
                print(f"  [+] Publishing post {aid}: {art['title']} (Due: {art['planned_publish_at']})")
            art_copy = dict(art)
            art_copy["published_at"] = pub_at
            published_arts.append(art_copy)
        else:
            # Must remain unpublished
            if not dry_run:
                remove_unpublished_article_files(art)

    print(f"[Scheduler] Total published: {len(published_arts)}/19. Newly released: {len(newly_published)}.")

    if dry_run:
        print("[Scheduler] Dry-run completed. No files modified.")
        return

    # Load article template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_html = f.read()

    pub_map = {a["id"]: a for a in published_arts}

    # Generate HTML for all published articles (or newly published)
    for art in published_arts:
        page_html = build_article_html(art, art["published_at"], pub_map, template_html)
        write_article_files(art, page_html)

    # Update listings & sitemap
    update_blog_listings(published_arts)
    update_sitemap(published_arts)

    # Save state
    save_state(state)
    print("[Scheduler] All outputs and sitemaps successfully synchronized.")


def print_status():
    """Print complete publishing schedule status table."""
    articles = load_all_article_definitions()
    state = get_or_create_state(articles)

    now = datetime.datetime.now(LONDON_TZ)
    print("\n" + "=" * 80)
    print("CORNERSTONE DIGITAL — BLOG PUBLISHING STATUS")
    print(f"System Clock: {now.isoformat()} ({TIMEZONE_STR})")
    print("=" * 80)
    print(f"{'ID':<4} {'Date':<12} {'Status':<12} {'Slug':<36}")
    print("-" * 80)

    next_release = None
    final_release = None

    for art in articles:
        aid = art["id"]
        st = state["articles"].get(aid, {})
        status = st.get("status", "scheduled")
        planned = art["planned_publish_at"]
        dt = parse_iso(planned)
        date_str = dt.strftime("%Y-%m-%d %H:%M")

        slug_trunc = (art["slug"][:33] + "...") if len(art["slug"]) > 36 else art["slug"]
        status_disp = f"✓ {status.upper()}" if status == "published" else f"⏳ {status.upper()}"
        print(f"{aid:<4} {date_str:<12} {status_disp:<12} {slug_trunc:<36}")

        if status == "scheduled" and next_release is None:
            next_release = (aid, art["title"], planned)
        if art["is_weekly_pack"]:
            final_release = (aid, art["title"], planned)

    print("-" * 80)
    if next_release:
        print(f"Next Scheduled Release: Post {next_release[0]} on {next_release[2]}")
        print(f"  Title: {next_release[1]}")
    else:
        print("All articles published.")
    if final_release:
        print(f"Final Scheduled Release: Post {final_release[0]} on {final_release[2]}")
        print(f"  Title: {final_release[1]}")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Cornerstone Digital Scheduled Publisher")
    parser.add_argument("--now", help="Simulate current ISO timestamp (e.g. 2026-10-26T09:00:00+00:00)")
    parser.add_argument("--status", action="store_true", help="Print schedule status table")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--publish-all", action="store_true", help="Publish all 19 articles")
    parser.add_argument("--reset", action="store_true", help="Reset to baseline 9 published posts")

    args = parser.parse_args()

    if args.status:
        print_status()
        return

    run_publisher(
        target_time=args.now,
        dry_run=args.dry_run,
        publish_all=args.publish_all,
        reset=args.reset
    )


if __name__ == "__main__":
    main()
