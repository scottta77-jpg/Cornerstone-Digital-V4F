# Core Web Vitals for small businesses: what to fix first

**Category:** Website performance

**Pillar:** Design & Build

**Author Name:** Cornerstone Digital

**Read Time Minutes:** 4

**Primary Query:** Core Web Vitals small business

**Slug:** core-web-vitals-small-business

**Seo Title:** Core Web Vitals for Small Businesses: What to Fix

**Meta Description:** Understand LCP, INP and CLS in plain English. Learn how to check Core Web Vitals and prioritise website fixes without chasing a perfect speed score.

**Excerpt:** Understand loading, responsiveness and layout stability, then prioritise the fixes that affect real customer journeys.

**Thumbnail:** thumbnails/06-core-web-vitals.webp

**Thumbnail Alt:** Yellow capsule moving through charcoal browser panels, illustrating responsive website performance.

## Article body

A slow website is frustrating when a customer is trying to check a service, open a menu or submit an enquiry. Core Web Vitals help you examine parts of that experience, but they are more useful as a diagnosis than as a trophy score.

**The short answer:** check how quickly the main content appears, how promptly the page responds and whether its layout moves unexpectedly. Use real visitor data where available, investigate problems with controlled tests and fix the important customer journeys first.

## What are LCP, INP and CLS?

Google's web.dev documentation describes three Core Web Vitals. Their “good” thresholds are assessed at the 75th percentile of visits, considered separately for mobile and desktop:

| Metric | What it measures | Good threshold |
| --- | --- | --- |
| Largest Contentful Paint, or LCP | When the largest visible content element appears | 2.5 seconds or less |
| Interaction to Next Paint, or INP | How quickly the page visually responds to interactions | 200 milliseconds or less |
| Cumulative Layout Shift, or CLS | Unexpected movement of page elements | 0.1 or less |

These are experience thresholds, not a requirement that every part of a page finish loading in under a second. [Source: web.dev](https://web.dev/articles/vitals).

## Begin with the pages customers actually use

Check the homepage, important service pages, popular articles and the booking or contact journey. A fast homepage does not tell you whether a booking widget becomes difficult to use on another page.

Use a phone as well as a desktop. Open menus, accept or reject optional cookies where relevant, navigate the page and complete the form. Record the problem you see before deciding how to fix it.

## Understand field data and lab tests

Field data reflects real visits across different devices and connections. A lab test runs in a controlled setup and helps reproduce a problem. They answer different questions, so the results may differ.

PageSpeed Insights can show available field data alongside lab diagnostics. Some smaller sites will not have enough public field data for a particular page. An absent result does not mean that the page has failed.

Use the diagnostics to identify likely causes, then check whether the change improves the experience. Avoid repeatedly tuning a page around one isolated test run.

## If the main content appears late

Investigate the element reported as LCP. Is it a large photograph, a banner or a block of text waiting for a font? Check the image size, delivery and loading behaviour, alongside server and rendering delays.

A large decorative video can add work without helping the customer make a decision. Consider whether a carefully chosen still image would serve the page better. Essential first-screen content should not be delayed by an unnecessary loading effect.

## If buttons and menus feel unresponsive

Look at the work the browser is doing around an interaction. Heavy scripts, complex animations and third-party widgets can contribute to delays. Remove tools that no longer serve a clear purpose.

Test essential integrations individually. A booking calendar or chat tool may be useful, but it still needs to work comfortably on an ordinary phone. Keep the customer action available if an optional widget fails.

## If the layout jumps while someone is using it

Reserve space for images, embeds and other content before it arrives. Watch banners, notices and font changes that unexpectedly move a button or paragraph.

A customer should not tap “Submit” and hit a different element because the layout changed. Reproduce the issue during the actual task, then confirm the fix on different screen sizes.

## Will passing guarantee better rankings?

No. Google says Core Web Vitals are used by its ranking systems, while good scores do not guarantee top rankings. Relevant, useful content and the wider search context still matter. [Source: Google Search Central](https://developers.google.com/search/docs/appearance/core-web-vitals).

The commercial benefit also needs measurement. If a form becomes easier to use, track successful submissions and qualified enquiries over a suitable period. Do not assume a universal percentage increase for every second removed.

## A sensible order for improvements

Fix broken customer actions first. Then address clearly poor performance on valuable pages, remove unnecessary weight and repeat the same tests. Monitor field results as new visits accumulate.

Keep a record of what changed and when. That helps separate a real improvement from changes in traffic, campaigns or test conditions. Combine performance work with our [website enquiry checks](/blog/website-not-generating-enquiries/) so the page is clear as well as responsive.

[Book a 15-minute discovery call](https://cornerstonedg.com/#booking) with Cornerstone Digital to discuss the performance problems affecting your customers.
