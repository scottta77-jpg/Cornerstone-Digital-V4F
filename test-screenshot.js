const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  
  const filePath = `file://${path.resolve('index.html')}`;
  await page.goto(filePath, { waitUntil: 'networkidle0' });
  
  // Scroll to footer to trigger animations
  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });
  
  // Wait a bit for animations
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  const footer = await page.$('.footer-section');
  if (footer) {
    await footer.screenshot({ path: 'footer-screenshot.png' });
    console.log('Screenshot saved to footer-screenshot.png');
  } else {
    console.log('Footer not found');
  }
  
  await browser.close();
})();
