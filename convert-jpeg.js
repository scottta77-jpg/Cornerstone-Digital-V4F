const sharp = require('sharp');
const fs = require('fs');

async function convert() {
  await sharp('assets/images/404-bg.jpeg')
    .webp({ quality: 80 })
    .toFile('assets/images/404-bg.webp');
  console.log("Converted 404-bg.jpeg to webp");
  fs.unlinkSync('assets/images/404-bg.jpeg');
  fs.unlinkSync('assets/images/404-template.jpeg');
}
convert();
