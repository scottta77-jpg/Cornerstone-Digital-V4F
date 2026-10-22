/**
 * Convert all homepage-referenced PNGs to WebP using sharp.
 * Originals are kept in place; .webp siblings are created alongside them.
 */
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const ROOT = __dirname;

// All PNGs referenced by index.html (local files only)
const targets = [
  // Services section
  'assets/images/services/services-background.png',
  'assets/images/services/design-build.png',
  'assets/images/services/technology.png',
  'assets/images/services/growth.png',
  'assets/images/services/strategy-consulting.png',

  // Projects section
  'assets/images/projects/oilbase-project.png',
  'assets/images/projects/herbert-crown-project.png',
  'assets/images/projects/herts-essex-pools-project.png',
  'assets/images/projects/crown-covenant-project.png',
  'assets/images/projects/impact-image.png',

  // Carousel
  'assets/images/carousel_1.png',
  'assets/images/carousel_2.png',
  'assets/images/carousel_3.png',
  'assets/images/carousel_4.png',

  // Impact image (from /images/ dir)
  'images/impact image 2.png',

  // Hero
  'assets/images/hero-poster.png',
  'assets/images/hero_bg_dark.png',

  // Logo
  'assets/images/cornerstone-logo-3.png',

  // OG preview
  'assets/images/cornerstone-og-preview.png',
];

async function convert(relPath) {
  const src = path.join(ROOT, relPath);
  if (!fs.existsSync(src)) {
    console.log(`  SKIP (not found): ${relPath}`);
    return;
  }

  const parsed = path.parse(src);
  const dest = path.join(parsed.dir, parsed.name + '.webp');

  const srcSize = fs.statSync(src).size;

  // Use quality 80 for photos, quality 85 for logos (smaller files)
  const isLogo = relPath.includes('logo');
  const quality = isLogo ? 90 : 80;

  await sharp(src)
    .webp({ quality, effort: 6 })
    .toFile(dest);

  const destSize = fs.statSync(dest).size;
  const savings = ((1 - destSize / srcSize) * 100).toFixed(1);

  console.log(`  ✓ ${relPath}`);
  console.log(`    ${(srcSize / 1024).toFixed(0)} KB → ${(destSize / 1024).toFixed(0)} KB  (−${savings}%)`);
}

(async () => {
  console.log('Converting PNGs to WebP...\n');
  for (const t of targets) {
    await convert(t);
  }
  console.log('\nDone!');
})();
