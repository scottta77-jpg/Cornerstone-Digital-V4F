const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  await page.setViewport({ width: 375, height: 812, deviceScaleFactor: 2 });
  await page.goto('http://localhost:3000/', { waitUntil: 'networkidle2' });
  await page.screenshot({ path: '/tmp/mobile-screen.png', fullPage: true });
  await browser.close();
  console.log("Screenshot saved to /tmp/mobile-screen.png");
})();
