#!/usr/bin/env python3
"""
Cornerstone Digital — Comprehensive Schedule & Article Verification Suite
Validates the entire 10-week publishing cycle, date boundaries, metadata,
schema JSON-LD, CTA buttons, sitemap, listings, and idempotence.
"""

import datetime
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLISHER = os.path.join(SCRIPT_DIR, "publish_scheduled_posts.py")

SCHEDULE = [
    ("10", "2026-10-26T09:00:00+00:00", "google-business-profile-vs-website"),
    ("11", "2026-11-02T09:00:00+00:00", "landing-page-vs-service-page"),
    ("12", "2026-11-09T09:00:00+00:00", "contact-form-questions-better-enquiries"),
    ("13", "2026-11-16T09:00:00+00:00", "track-marketing-paying-customers"),
    ("14", "2026-11-23T09:00:00+00:00", "website-maintenance-after-launch"),
    ("15", "2026-11-30T09:00:00+00:00", "ai-chatbot-vs-live-chat"),
    ("16", "2026-12-07T09:00:00+00:00", "useful-service-area-pages"),
    ("17", "2026-12-14T09:00:00+00:00", "customer-case-study-guide"),
    ("18", "2026-12-21T09:00:00+00:00", "christmas-opening-hours-website-bookings"),
    ("19", "2026-12-28T09:00:00+00:00", "90-day-digital-marketing-plan-small-business"),
]


def run_cmd(args):
    res = subprocess.run([sys.executable, PUBLISHER] + args, capture_output=True, text=True, cwd=SCRIPT_DIR)
    if res.returncode != 0:
        print(f"Error running {args}: {res.stderr}")
    return res


def test_baseline():
    print("\n--- TEST 1: Baseline Pre-Release Verification (Current Time: 21 Oct 2026) ---")
    run_cmd(["--reset"])
    run_cmd([]) # evaluate against current clock

    with open(os.path.join(SCRIPT_DIR, "publishing-state.json")) as f:
        state = json.load(f)

    # Check that posts 01-09 are published and 10-19 are scheduled
    for i in range(1, 10):
        aid = f"{i:02d}"
        assert state["articles"][aid]["status"] == "published", f"Post {aid} should be published"
    for i in range(10, 20):
        aid = str(i)
        assert state["articles"][aid]["status"] == "scheduled", f"Post {aid} should be scheduled"

    # Verify no post 10-19 files exist on disk
    for pid, _, slug in SCHEDULE:
        f_html = os.path.join(SCRIPT_DIR, "blog", f"{slug}.html")
        f_idx = os.path.join(SCRIPT_DIR, "blog", slug, "index.html")
        assert not os.path.exists(f_html), f"Future file {f_html} should NOT exist!"
        assert not os.path.exists(f_idx), f"Future dir {f_idx} should NOT exist!"

    # Verify sitemap contains 01-09 only
    with open(os.path.join(SCRIPT_DIR, "sitemap.xml")) as f:
        sitemap = f.read()
    assert "website-not-generating-enquiries" in sitemap
    assert "google-business-profile-vs-website" not in sitemap

    # Verify blogs listing contains 01-09 only
    with open(os.path.join(SCRIPT_DIR, "blogs", "index.html")) as f:
        blogs_html = f.read()
    assert "google-business-profile-vs-website" not in blogs_html

    print("✓ Baseline PASSED: Posts 10–19 strictly unreleased, routes non-existent, sitemap clean.")


def test_boundary_week_1():
    print("\n--- TEST 2: Week 1 Boundary Verification (26 Oct 2026 09:00) ---")
    # 1 second before release
    run_cmd(["--now", "2026-10-26T08:59:59+00:00"])
    f_html = os.path.join(SCRIPT_DIR, "blog", "google-business-profile-vs-website.html")
    assert not os.path.exists(f_html), "Post 10 should NOT exist before 09:00:00"

    # Exactly at release time
    res = run_cmd(["--now", "2026-10-26T09:00:00+00:00"])
    assert "Publishing post 10" in res.stdout
    assert os.path.exists(f_html), "Post 10 should exist at 09:00:00"

    # Post 11 should still NOT exist
    p11_html = os.path.join(SCRIPT_DIR, "blog", "landing-page-vs-service-page.html")
    assert not os.path.exists(p11_html), "Post 11 should NOT exist"

    # Verify content of Post 10
    with open(f_html) as f:
        content = f.read()

    assert "BOOK YOUR 15-MINUTE DISCOVERY CALL" in content, "CTA button missing"
    assert "https://cornerstonedg.com/#booking" in content, "CTA link missing"
    assert "cornerstone-blog-cta__button" in content, "CTA button class missing"
    assert '"datePublished": "2026-10-26T09:00:00+00:00"' in content, "JSON-LD datePublished missing"
    assert '<meta property="og:url" content="https://cornerstonedg.com/blog/google-business-profile-vs-website/"/>' in content, "og:url mismatch"
    assert '<link rel="canonical" href="https://cornerstonedg.com/blog/google-business-profile-vs-website/"/>' in content, "canonical link mismatch"
    assert "/assets/images/blog/10-google-profile-website.webp" in content, "thumbnail missing"

    # Verify post 10 is in sitemap and blogs index
    with open(os.path.join(SCRIPT_DIR, "sitemap.xml")) as f:
        sitemap = f.read()
    assert "google-business-profile-vs-website" in sitemap
    assert "landing-page-vs-service-page" not in sitemap

    with open(os.path.join(SCRIPT_DIR, "blogs", "index.html")) as f:
        blogs_html = f.read()
    assert "google-business-profile-vs-website" in blogs_html
    assert "landing-page-vs-service-page" not in blogs_html

    print("✓ Week 1 Boundary PASSED: Post 10 published with accurate metadata/CTA; Post 11 blocked.")


def test_idempotence():
    print("\n--- TEST 3: Idempotence Verification (Re-running at same time) ---")
    res = run_cmd(["--now", "2026-10-26T09:05:00+00:00"])
    assert "Newly released: 0" in res.stdout, "Re-running should release 0 new posts"

    with open(os.path.join(SCRIPT_DIR, "sitemap.xml")) as f:
        sitemap = f.read()
    count = sitemap.count("google-business-profile-vs-website")
    assert count == 1, f"Expected 1 sitemap entry, found {count}"

    with open(os.path.join(SCRIPT_DIR, "blogs", "index.html")) as f:
        blogs_html = f.read()
    card_count = blogs_html.count('href="/blog/google-business-profile-vs-website"')
    assert card_count == 1, f"Expected 1 card in blogs listing, found {card_count}"

    print("✓ Idempotence PASSED: Re-running produces zero duplicates and leaves state untouched.")


def test_full_ten_week_progression():
    print("\n--- TEST 4: Full 10-Week Progressive Publishing Verification ---")
    run_cmd(["--reset"])

    total_released = 9
    for week_idx, (pid, planned_dt, slug) in enumerate(SCHEDULE, 1):
        res = run_cmd(["--now", planned_dt])
        total_released += 1
        assert f"Publishing post {pid}" in res.stdout
        assert f"Total published: {total_released}/19" in res.stdout

        # Verify article exists
        f_html = os.path.join(SCRIPT_DIR, "blog", f"{slug}.html")
        assert os.path.exists(f_html), f"Article {slug}.html was not created"

        # Verify in sitemap
        with open(os.path.join(SCRIPT_DIR, "sitemap.xml")) as f:
            sitemap = f.read()
        assert slug in sitemap

        # Check next week post does not exist yet (if not last week)
        if week_idx < len(SCHEDULE):
            next_slug = SCHEDULE[week_idx][2]
            next_html = os.path.join(SCRIPT_DIR, "blog", f"{next_slug}.html")
            assert not os.path.exists(next_html), f"Next week article {next_slug} should not exist yet"

    # Check after final release (e.g. 2027-01-04)
    res = run_cmd(["--now", "2027-01-04T09:00:00+00:00"])
    assert "Total published: 19/19" in res.stdout
    assert "Newly released: 0" in res.stdout

    print("✓ 10-Week Progression PASSED: Exactly 1 article released each Monday; stops at Post 19.")


def main():
    print("=" * 70)
    print("RUNNING CORNERSTONE DIGITAL PUBLISHING VERIFICATION SUITE")
    print("=" * 70)

    try:
        test_baseline()
        test_boundary_week_1()
        test_idempotence()
        test_full_ten_week_progression()

        # Finally, reset back to baseline so the site is clean for production
        print("\n--- TEARDOWN: Resetting repository to baseline for production ---")
        run_cmd(["--reset"])
        run_cmd([])
        print("✓ Repository reset to clean baseline (posts 01-09 published, 10-19 scheduled).")

        print("\n" + "=" * 70)
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (4/4)")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
