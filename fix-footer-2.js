const fs = require('fs');
const path = require('path');

const filesToFix = [
  'services/index.html',
  'projects/index.html',
  'privacy-policy/index.html',
  'terms-and-conditions/index.html',
  '404.html',
  '404/index.html',
  'project/ecosphere/index.html'
];

for (const file of filesToFix) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    const oldBlockRegex = /<div style="margin-top: 16px; display: flex; flex-direction: column; gap: 8px;">\s*<a href="tel:07482765599"[\s\S]*?<\/p>\s*<\/div>/g;
    content = content.replace(oldBlockRegex, '');
    
    // This matches the <div class="footer-menus"> regardless of attributes before/after
    const footerMenuRegex = /(<div[^>]*class="footer-menus"[^>]*>)\s*(<div[^>]*class="footer-extra-link"[^>]*>)/i;
    
    const replacement = `$1
            <div fade-up="true" class="footer-extra-link" style="display: flex; flex-direction: column; gap: 16px;">
              <h6 class="text-white" style="font-size: 1.25rem; font-weight: 600; margin-bottom: 8px; color: white;">Contact Us</h6>
              <a href="tel:07482765599" class="footer-link-style-two">07482 765599</a>
              <span class="footer-link-style-two">1 Paul road, Essex , SO1 8EL, London</span>
            </div>
            
            <div fade-up="true" class="footer-extra-link" style="display: flex; flex-direction: column; gap: 16px;">
              <h6 class="text-white" style="font-size: 1.25rem; font-weight: 600; margin-bottom: 8px; color: white;">Legal</h6>`;
    
    if (footerMenuRegex.test(content)) {
      content = content.replace(footerMenuRegex, replacement);
      fs.writeFileSync(filePath, content, 'utf8');
      console.log('Fixed', file);
    } else {
      console.log('Regex not matched in', file);
    }
  }
}
