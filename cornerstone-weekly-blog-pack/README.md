# Cornerstone Digital: ten-week blog publishing pack

Ten complete new articles, ten original thumbnails and a Monday release plan. Prepared 21 October 2026. The pack supplements the earlier nine-post collection.

## Start here

Give this folder to Antigravity with the Cornerstone Digital website project open. Use `ANTIGRAVITY-PROMPT.md` as the accompanying implementation prompt.

- `01-publishing-calendar.md`: all ten Mondays, dates and article titles.
- `02-all-articles.md`: all ten articles in one editable text file, with SEO titles, descriptions and excerpts.
- `03-research-and-editorial-notes.md`: competitor resources, primary sources, topic selection and editorial reasoning.
- `04-scheduling-and-technical-checklist.md`: actual scheduling, visibility rules, schema, CTA and verification requirements.
- `posts/`: individual Markdown articles and HTML body fragments.
- `thumbnails/`: matching original PNGs and WebP exports.
- `cms-content.json`: portable article data and proposed schedule fields; it needs mapping to the actual CMS.
- `publishing-schedule.json`: exact Monday-to-post mapping, with a proposed 09:00 Europe/London default.
- `schema-blueprints.json`: BlogPosting descriptions for integration with real CMS dates and final image URLs.
- `existing-post-reference.json`: IDs and routes from the earlier nine-post pack, for link mapping.
- `cta-block.html`: reusable yellow booking-button styles and structure.
- `thumbnail-prompts.md`: the prompt used for each original image.
- `Cornerstone-Digital-10-Week-Review.html`: a self-contained reading copy with images, calendar and implementation notes.

## Publication status

The ten Monday dates run from 26 October to 28 December 2026. The user specified the day and cadence, not the hour; 09:00 is a proposed implementation default. The articles are prepared as drafts with planned publishing dates. Live scheduling has not been activated and the website has not been changed from this chat. Antigravity must configure and verify the real scheduler as part of implementation.

`date_published` and `date_modified` are empty in the draft source. Populate them with real values at publication. Use `planned_publish_at` to schedule, not to imply the article is already public. Reading times use the article text at 220 words per minute.

The HTML reading copy intentionally shows all ten future posts for review. Its in-pack article links navigate to sections of the reading copy. The CMS files retain the proposed website routes and must be released according to the schedule.
