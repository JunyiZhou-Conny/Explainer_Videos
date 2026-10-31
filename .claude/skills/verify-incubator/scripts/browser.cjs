#!/usr/bin/env node
// Drive a Studio page with Playwright from a JSON list of steps; save every proof.
//   node browser.cjs <steps.json> <evidence-dir> <name> [base-url]
// Steps (relative URLs resolve against base-url, the served Studio site):
//   {"goto": "index.html"}                       open a page; waits for network idle
//   {"click": "role=link[name=\"视频库\"]"}        any Playwright selector
//   {"fill": "#question", "value": "..."}
//   {"check": "input[name=agent][value=manual-other]"}
//   {"wait": "#promptText"}                       until visible
//   {"expect": "h1", "text": "制作进度"}           visible element containing the text
//   {"expectCount": ".ep", "min": 1}              at least min matching elements
//   {"shot": "board"}                             <name>-board.png (full page)
//   {"aria": "board", "of": "main"}               <name>-board.aria.txt (ARIA snapshot)
//   {"save": "prompt", "of": "#promptText"}       <name>-prompt.txt (innerText)
//   {"popup": "role=button[name=\"生成 issue →\"]", "as": "issue", "params": {"template": "episode-request.yml"}}
//        click, catch the window it opens, save <name>-issue.json (url + query params) and
//        require each listed param to contain its value. github.com is stubbed: no request leaves.
//   {"dialog": "role=button[name=\"生成 issue →\"]", "text": "必填"}
//        click and require an alert/confirm whose message contains the text
// Exits 1 on the first failed step; <name>.steps.json records every step and its result.
const fs = require('fs');
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) {
  console.error('playwright is not installed here: run `npm i -g playwright && npx playwright install chromium`');
  process.exit(2);
}

(async () => {
  const [stepsFile, outDir, name, base = ''] = process.argv.slice(2);
  const steps = JSON.parse(fs.readFileSync(stepsFile, 'utf8'));
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'zh-CN' });
  await context.route('https://github.com/**', r => r.fulfill({ status: 200, contentType: 'text/html', body: 'stub' }));
  const page = await context.newPage();
  let lastDialog = null;
  page.on('dialog', d => { lastDialog = d.message(); d.dismiss().catch(() => {}); });
  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => consoleErrors.push(String(e)));
  const log = [];
  const file = suffix => path.join(outDir, `${name}-${suffix}`);
  let failed = false;
  for (const step of steps) {
    const entry = { step, ok: true };
    try {
      if (step.goto) {
        await page.goto(new URL(step.goto, base || undefined).href, { waitUntil: 'networkidle' });
        entry.url = page.url();
      } else if (step.click) await page.locator(step.click).first().click();
      else if (step.fill) await page.locator(step.fill).fill(step.value);
      else if (step.check) await page.locator(step.check).check();
      else if (step.wait) await page.locator(step.wait).first().waitFor({ state: 'visible', timeout: 10000 });
      else if (step.expect) {
        const hit = page.locator(step.expect, { hasText: step.text }).first();
        await hit.waitFor({ state: 'visible', timeout: 10000 });
        entry.found = (await hit.innerText()).slice(0, 200);
      } else if (step.expectCount) {
        const n = await page.locator(step.expectCount).count();
        entry.count = n;
        if (n < (step.min ?? 1)) throw new Error(`${step.expectCount}: ${n} < ${step.min ?? 1}`);
      } else if (step.shot) {
        await page.screenshot({ path: file(`${step.shot}.png`), fullPage: true });
        entry.saved = file(`${step.shot}.png`);
      } else if (step.aria) {
        fs.writeFileSync(file(`${step.aria}.aria.txt`), await page.locator(step.of || 'body').ariaSnapshot());
        entry.saved = file(`${step.aria}.aria.txt`);
      } else if (step.save) {
        fs.writeFileSync(file(`${step.save}.txt`), await page.locator(step.of).first().innerText());
        entry.saved = file(`${step.save}.txt`);
      } else if (step.popup) {
        const [popup] = await Promise.all([context.waitForEvent('page'), page.locator(step.popup).first().click()]);
        await popup.waitForURL(/^https?:/, { timeout: 10000 });
        const url = new URL(popup.url());
        const params = Object.fromEntries(url.searchParams);
        fs.writeFileSync(file(`${step.as}.json`), JSON.stringify({ url: url.href, params }, null, 2));
        entry.saved = file(`${step.as}.json`);
        for (const [k, want] of Object.entries(step.params || {}))
          if (!(params[k] || '').includes(want)) throw new Error(`param ${k}=${JSON.stringify(params[k])} lacks ${JSON.stringify(want)}`);
        await popup.close();
      } else if (step.dialog) {
        lastDialog = null;
        await page.locator(step.dialog).first().click();
        for (let i = 0; i < 50 && lastDialog === null; i++) await page.waitForTimeout(100);
        entry.dialog = lastDialog;
        if (lastDialog === null || !lastDialog.includes(step.text)) throw new Error(`dialog ${JSON.stringify(lastDialog)} lacks ${JSON.stringify(step.text)}`);
      } else throw new Error('unknown step');
    } catch (e) {
      entry.ok = false; entry.error = String(e).split('\n')[0];
      failed = true;
    }
    log.push(entry);
    console.log(`${entry.ok ? 'ok  ' : 'FAIL'} ${JSON.stringify(step)}${entry.error ? '  ' + entry.error : ''}`);
    if (failed) { await page.screenshot({ path: file('failure.png'), fullPage: true }).catch(() => {}); break; }
  }
  if (consoleErrors.length) console.log(`console errors: ${JSON.stringify(consoleErrors)}`);
  fs.writeFileSync(path.join(outDir, `${name}.steps.json`), JSON.stringify({ log, consoleErrors }, null, 2));
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
