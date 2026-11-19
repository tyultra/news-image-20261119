// Screenshot build/frontpage.html to ../entry.png at exactly 1024x1024.
import { chromium } from 'playwright-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(__dirname, '..');
const html = path.join(repo, 'build', 'frontpage.html');
const out = path.join(repo, 'entry.png');

const browser = await chromium.launch({
  executablePath: '/usr/bin/google-chrome',
  args: ['--no-sandbox', '--disable-gpu'],
});
const page = await browser.newPage({
  viewport: { width: 1024, height: 1024 },
  deviceScaleFactor: 1,
});
await page.goto('file://' + html);
await page.waitForTimeout(400);
await page.screenshot({ path: out });
await browser.close();
console.log('wrote', out);
