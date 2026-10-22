const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox','--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  
  // OG image standard size is 1200x630
  await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
  
  // Load local file
  await page.goto('file:///Users/boyka777/Cornerstone%20Digital%20V4F/Cornerstone%20Digital%20V4F/build_og.html', { waitUntil: 'networkidle2' });
  
  // Optional: wait a moment for fonts to load
  await new Promise(r => setTimeout(r, 2000));
  
  // Save as high-quality image
  await page.screenshot({ path: '/Users/boyka777/Cornerstone Digital V4F/Cornerstone Digital V4F/assets/images/cornerstone-og-preview.png', type: 'png' });
  
  await browser.close();
  console.log('OG preview screenshot saved successfully.');
})();
