# Scheduling and technical checklist

## Status and requested dates

This folder contains ten finished articles and a prepared publishing schedule. It does not itself create a live website scheduler. No live publishing task has been activated from this chat. Antigravity must implement and verify the schedule in the existing website project or CMS.

Publish one article each Monday on these ten dates: 26 October; 2, 9, 16, 23 and 30 November; 7, 14, 21 and 28 December 2026. Use `publishing-schedule.json` as the authoritative mapping of dates to posts.

The proposed default hour is **09:00 Europe/London**. The user specified the dates and cadence, not a clock time. Keep the hour in one configurable setting if a different time is chosen. All ten supplied timestamps fall after the UK autumn clock change and therefore use UTC+00:00. Preserve the IANA timezone rather than assuming every future date is always GMT.

Append posts 10–19 to the existing collection. Keep the earlier nine posts and their assets intact.

## Use the existing publishing architecture

Prefer the CMS's native scheduled-publication feature where available. Import each post as a draft, map its fields, upload its image and then set its assigned scheduled time. Confirm the CMS actually reports a scheduled state for all ten records.

If the site is static, implement an appropriate timed build/deployment or server-controlled publishing mechanism through the existing hosting workflow. A date filter evaluated only at build time does not update a deployed site by itself. A client-side filter that hides cards does not keep article HTML or sitemap entries from being published early.

Use the actual available infrastructure and credentials. Do not invent a CMS connection or report scheduling as successful because the JSON file contains dates. If live activation is blocked, identify the exact missing access/configuration while completing the content implementation and local verification.

## Visibility requirements

Before an article's release, keep it out of the public listing, featured slot, related-article widgets, sitemap, RSS/feed and public article output. Authenticated previews can remain available. At the release, publish the article and relevant discovery surfaces together. Check any cache or rebuild dependency.

Use a combination of publication state and the due timestamp. Keep the process safe to run again: the same post must not be created twice, and a previously published date must not reset on every build. Publish only the ten supplied posts and stop adding releases after 28 December 2026.

If setup occurs after an assigned date or a release is missed, surface it for an explicit decision. Do not silently publish several overdue posts together or backdate an actual publication timestamp.

## Metadata and schema

Map the title, excerpt, category, reading time, author, SEO title, description, slug, image and related-post fields. Use Cornerstone Digital as the organisation author and publisher. Set the canonical URL and social-sharing image from the final site output.

Use the `schema` object in each entry of `schema-blueprints.json` as the basis of a `<script type="application/ld+json">` block. The outer editorial instruction fields are not schema. Populate real `datePublished` and `dateModified` values and the final public image URL. Keep markup consistent with the visible article and consolidate existing Article markup rather than duplicating it.

Do not emit public Article JSON-LD for an unpublished page. Do not add FAQ markup to promise Google FAQ rich results or claim that markup guarantees indexing or AI recommendations.

## Images, layout and shared CTA

Use each post's matching WebP asset; retain the PNG original. Preserve the established dark/yellow visual system and existing article/sidebar layout. Reserve image dimensions, provide suitable responsive sizes and choose alt text according to how the image is used.

The supplied article body already ends in the booking CTA. Render that closing link as the shared high-contrast yellow component using `cta-block.html`, rather than adding a second copy.

- Label: `BOOK YOUR 15-MINUTE DISCOVERY CALL →`
- Target: `https://cornerstonedg.com/#booking`
- Position: after the article's final content section and before related articles.
- Preserve keyboard focus, adequate text contrast and a comfortable touch target.

Search case-insensitively for leftover Olyyx business branding in templates, globals, metadata and structured data. Replace business references appropriately while preserving any licence-required attribution.

## Verify the schedule, not only the article template

Use a staging clock/test date or the CMS preview facilities where available:

1. Before 26 October 2026 at the configured hour: none of posts 10–19 is publicly released.
2. At the first release: only post 10 is added.
3. Before and after a later Monday boundary: precisely the assigned next post becomes available.
4. At 28 December's release: all ten are available, with no eleventh release.
5. Re-running publication does not duplicate records or reset dates.
6. Unpublished posts do not appear in generated routes, sitemap, feeds, listing or related links.
7. Released article routes, images, metadata and booking links work on desktop and mobile.

Run the project's relevant build and validation checks. Report the mechanism used, timezone, actual scheduled states, next release, last release and evidence that automatic publication is active. If it is not active, state that plainly.
