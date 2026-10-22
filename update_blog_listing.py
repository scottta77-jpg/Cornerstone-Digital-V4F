import json
import os
import re

def update_blog_listing():
    root_dir = "/Users/boyka777/Cornerstone Digital V4F/Cornerstone Digital V4F"
    pack_dir = "/Users/boyka777/Cornerstone Digital V4F/cornerstone-blog-pack"

    with open(os.path.join(pack_dir, "cms-content.json"), "r", encoding="utf-8") as f:
        articles = json.load(f)

    art_map = {art["id"]: art for art in articles}

    # Post 01 is Featured
    p01 = art_map["01"]

    # Posts 02 through 09 are Cards 1-8
    card_posts = [art_map[f"{i:02d}"] for i in range(2, 10)]

    listing_path = os.path.join(root_dir, "blogs", "index.html")
    with open(listing_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Title & Meta
    html = re.sub(
        r'<title>.*?</title>',
        '<title>Blogs | Cornerstone Digital</title>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" name="description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." name="description"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" property="og:title"/>',
        '<meta content="Blogs | Cornerstone Digital" property="og:title"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" property="og:description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." property="og:description"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" property="og:image"/>',
        '<meta content="https://cornerstonedg.com/assets/images/blog/01-website-enquiries.webp" property="og:image"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" name="twitter:title"/>',
        '<meta content="Blogs | Cornerstone Digital" name="twitter:title"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" name="twitter:description"/>',
        '<meta content="Practical guides and insights on website design, business automation, local SEO and conversion strategy for growing service businesses." name="twitter:description"/>',
        html
    )
    html = re.sub(
        r'<meta content=".*?" name="twitter:image"/>',
        '<meta content="https://cornerstonedg.com/assets/images/blog/01-website-enquiries.webp" name="twitter:image"/>',
        html
    )

    # Canonical
    if '<link rel="canonical"' in html:
        html = re.sub(r'<link rel="canonical".*?/>', '<link rel="canonical" href="https://cornerstonedg.com/blogs/"/>', html)
    else:
        html = html.replace('</head>', '<link rel="canonical" href="https://cornerstonedg.com/blogs/"/>\n</head>')

    # 2. Update JSON-LD ItemList
    item_list_elements = []
    for idx, art in enumerate(articles, 1):
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

    # 3. Update Hero / Featured Section
    # Headline & Excerpt
    old_hero_regex = r'<h1 class="h1">\s*The Future of\s*</h1>\s*<div class="h1">\s*Dark Mode in 2026\s*</div>'
    new_hero_headline = f'<h1 class="h1">\n                Why your website isn\'t\n              </h1>\n<div class="h1">\n                generating enquiries\n              </div>'
    html = re.sub(old_hero_regex, new_hero_headline, html)

    old_hero_para_regex = r'<p class="text-regular" group-fade-up-item="true">\s*Explore how high-contrast dark aesthetics.*?</p>'
    new_hero_para = f'<p class="text-regular" group-fade-up-item="true">\n              {p01["excerpt"]}\n            </p>'
    html = re.sub(old_hero_para_regex, new_hero_para, html, flags=re.DOTALL)

    # Button href
    old_btn_regex = r'(<a class="button w-inline-block"[^>]*href=")#(")'
    html = re.sub(old_btn_regex, r'\g<1>/blog/website-not-generating-enquiries\g<2>', html)

    # Hero background image
    old_hero_bg_regex = r'<div class="blog-hero-bg">\s*<img alt="Banner"[^>]*/>'
    new_hero_bg = f'<div class="blog-hero-bg">\n<img alt="{p01["title"]}" class="cover-size-image" loading="lazy" sizes="100vw" width="1672" height="941" src="/assets/images/blog/01-website-enquiries.webp"/>'
    html = re.sub(old_hero_bg_regex, new_hero_bg, html)

    # 4. Update the 8 Cards
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

    # Cornerstone Digital Blog Pagination CSS
    pagination_css = """
      /* Cornerstone Digital Blog Pagination */
      .cornerstone-pagination-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-top: 56px;
        margin-bottom: 24px;
        padding: 0 16px;
        flex-wrap: wrap;
        width: 100%;
        position: relative;
        z-index: 5;
      }
      .cornerstone-pagination-numbers {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .cornerstone-page-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        padding: 0;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 6px;
        color: #ffffff;
        font-family: 'Space Grotesk', 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
        user-select: none;
        outline: none;
      }
      .cornerstone-page-number:hover:not(.is-active) {
        background: rgba(240, 226, 38, 0.08);
        border-color: #F0E226;
        color: #F0E226;
        transform: translateY(-2px);
      }
      .cornerstone-page-number.is-active {
        background: #F0E226;
        border-color: #F0E226;
        color: #111112;
        font-weight: 700;
        box-shadow: 0 4px 18px rgba(240, 226, 38, 0.28);
        cursor: default;
        pointer-events: none;
      }
      .cornerstone-page-number:focus-visible,
      .cornerstone-pagination-btn:focus-visible {
        outline: 2px solid #F0E226;
        outline-offset: 3px;
      }
      .cornerstone-pagination-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        height: 48px;
        padding: 0 22px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 6px;
        color: #ffffff;
        font-family: 'Space Grotesk', 'DM Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
        user-select: none;
        outline: none;
      }
      .cornerstone-pagination-btn svg {
        transition: transform 0.25s ease;
      }
      .cornerstone-pagination-btn:hover:not(:disabled):not(.is-disabled) {
        background: #F0E226;
        border-color: #F0E226;
        color: #111112;
        transform: translateY(-2px);
        box-shadow: 0 4px 18px rgba(240, 226, 38, 0.28);
      }
      .cornerstone-pagination-btn.prev-btn:hover:not(:disabled):not(.is-disabled) svg {
        transform: translateX(-3px);
      }
      .cornerstone-pagination-btn.next-btn:hover:not(:disabled):not(.is-disabled) svg {
        transform: translateX(3px);
      }
      .cornerstone-pagination-btn:disabled,
      .cornerstone-pagination-btn.is-disabled {
        opacity: 0.28;
        cursor: not-allowed;
        pointer-events: none;
        border-color: rgba(255, 255, 255, 0.06);
        background: transparent;
        transform: none;
      }
      .cornerstone-pagination-info {
        width: 100%;
        text-align: center;
        margin-top: 12px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.45);
        letter-spacing: 0.02em;
      }
      @media (max-width: 600px) {
        .cornerstone-pagination-wrap {
          gap: 8px;
          margin-top: 40px;
        }
        .cornerstone-page-number {
          width: 42px;
          height: 42px;
          font-size: 0.9rem;
        }
        .cornerstone-pagination-btn {
          height: 42px;
          padding: 0 14px;
          font-size: 0.8rem;
        }
        .cornerstone-pagination-btn span {
          display: none;
        }
      }
    """

    # Inject pagination CSS into head if not already present
    if ".cornerstone-pagination-wrap" not in html:
        html = html.replace("</style>", f"{pagination_css}\n</style>")

    # Pagination HTML placed below the cards inside .w-dyn-list
    pagination_html = """<nav class="cornerstone-pagination-wrap" aria-label="Blog pagination" role="navigation">
  <button class="cornerstone-pagination-btn prev-btn is-disabled" id="blog-prev-btn" aria-label="Previous page" disabled>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <line x1="19" y1="12" x2="5" y2="12"></line>
      <polyline points="12 19 5 12 12 5"></polyline>
    </svg>
    <span>Previous</span>
  </button>
  <div class="cornerstone-pagination-numbers" id="blog-pagination-numbers">
    <button class="cornerstone-page-number is-active" data-page="1" aria-current="page" aria-label="Page 1">1</button>
  </div>
  <button class="cornerstone-pagination-btn next-btn is-disabled" id="blog-next-btn" aria-label="Next page" disabled>
    <span>Next</span>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12"></line>
      <polyline points="12 5 19 12 12 19"></polyline>
    </svg>
  </button>
  <div class="cornerstone-pagination-info" id="blog-pagination-info">Showing all 8 articles</div>
</nav>"""

    # Pagination Script
    pagination_js = """<script id="cornerstone-pagination-script">
(function() {
  function initPagination() {
    var POSTS_PER_PAGE = 8;
    var listContainer = document.querySelector(".blog-collection-list");
    if (!listContainer) return;

    var items = Array.from(listContainer.querySelectorAll(".w-dyn-item"));
    var totalItems = items.length;
    if (totalItems === 0) return;

    var totalPages = Math.ceil(totalItems / POSTS_PER_PAGE);
    var prevBtn = document.getElementById("blog-prev-btn");
    var nextBtn = document.getElementById("blog-next-btn");
    var numbersContainer = document.getElementById("blog-pagination-numbers");
    var infoEl = document.getElementById("blog-pagination-info");

    var urlParams = new URLSearchParams(window.location.search);
    var currentPage = parseInt(urlParams.get("page"), 10) || 1;
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    function renderPagination() {
      var startIndex = (currentPage - 1) * POSTS_PER_PAGE;
      var endIndex = Math.min(startIndex + POSTS_PER_PAGE, totalItems);

      items.forEach(function(item, index) {
        if (index >= startIndex && index < endIndex) {
          item.style.display = "";
          item.style.opacity = "1";
          item.style.visibility = "visible";
          item.style.transform = "none";
        } else {
          item.style.display = "none";
        }
      });

      if (numbersContainer) {
        numbersContainer.innerHTML = "";
        for (var i = 1; i <= totalPages; i++) {
          (function(pageIdx) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "cornerstone-page-number" + (pageIdx === currentPage ? " is-active" : "");
            btn.setAttribute("data-page", pageIdx);
            btn.setAttribute("aria-label", "Page " + pageIdx);
            if (pageIdx === currentPage) {
              btn.setAttribute("aria-current", "page");
            }
            btn.textContent = pageIdx;
            btn.addEventListener("click", function() {
              goToPage(pageIdx);
            });
            numbersContainer.appendChild(btn);
          })(i);
        }
      }

      if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
        if (currentPage <= 1) {
          prevBtn.classList.add("is-disabled");
        } else {
          prevBtn.classList.remove("is-disabled");
        }
      }

      if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
        if (currentPage >= totalPages) {
          nextBtn.classList.add("is-disabled");
        } else {
          nextBtn.classList.remove("is-disabled");
        }
      }

      if (infoEl) {
        if (totalItems <= POSTS_PER_PAGE) {
          infoEl.textContent = "Showing all " + totalItems + " articles";
        } else {
          infoEl.textContent = "Showing " + (startIndex + 1) + "–" + endIndex + " of " + totalItems + " articles";
        }
      }
    }

    function goToPage(page) {
      if (page < 1 || page > totalPages || page === currentPage) return;
      currentPage = page;

      var url = new URL(window.location);
      if (currentPage === 1) {
        url.searchParams.delete("page");
      } else {
        url.searchParams.set("page", currentPage);
      }
      window.history.pushState({ page: currentPage }, "", url);

      renderPagination();

      var section = document.querySelector(".blog-arcive-section");
      if (section) {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    if (prevBtn) {
      prevBtn.onclick = function() {
        goToPage(currentPage - 1);
      };
    }

    if (nextBtn) {
      nextBtn.onclick = function() {
        goToPage(currentPage + 1);
      };
    }

    window.addEventListener("popstate", function(e) {
      var page = (e.state && e.state.page) || parseInt(new URLSearchParams(window.location.search).get("page"), 10) || 1;
      currentPage = page;
      renderPagination();
    });

    renderPagination();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPagination);
  } else {
    initPagination();
  }
})();
</script>"""

    # Replace collection list and append pagination HTML
    old_cards_regex = r'<div class="blog-collection-list w-dyn-items" role="list">.*?</div>\s*(?:<nav class="cornerstone-pagination-wrap".*?</nav>\s*)?</div>\s*</div>\s*</div>\s*</section>'
    new_cards_block = f'<div class="blog-collection-list w-dyn-items" role="list">\n{all_cards_html}\n</div>\n{pagination_html}\n</div>\n</div>\n</div>\n</section>'
    html = re.sub(old_cards_regex, new_cards_block, html, flags=re.DOTALL)

    # Inject pagination script before </body> if not present, or replace existing
    if '<script id="cornerstone-pagination-script">' in html:
        html = re.sub(r'<script id="cornerstone-pagination-script">.*?</script>', pagination_js, html, flags=re.DOTALL)
    else:
        html = html.replace("</body>", f"{pagination_js}\n</body>")

    # Save to blogs/index.html, blog.html, and blog/index.html
    with open(listing_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated blogs/index.html")

    blog_html_path = os.path.join(root_dir, "blog.html")
    with open(blog_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated blog.html")

    blog_index_path = os.path.join(root_dir, "blog", "index.html")
    with open(blog_index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated blog/index.html")

if __name__ == "__main__":
    update_blog_listing()
