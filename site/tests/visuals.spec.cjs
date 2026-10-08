const { test, expect } = require("@playwright/test");

test("navigation works with keyboard and preserves deep links", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/#type");
  await expect(page.getByRole("tabpanel", { name: "Type" })).toBeVisible();
  await page.getByRole("tab", { name: "Type", exact: true }).focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByRole("tab", { name: "Icons", exact: true })).toBeFocused();
  await expect(page.getByRole("tabpanel", { name: "Icons" })).toBeVisible();
  await page.keyboard.press("End");
  await expect(page.getByRole("tabpanel", { name: "Examples" })).toBeVisible();
  expect(errors).toEqual([]);
});

test("font cuts use their own glyphs and disclose unsupported input", async ({ page }) => {
  await page.goto("/#type");
  await page.locator("#sample").fill("SUNRISE");
  await expect(page.locator("#unsupported")).toContainText("Outside this cut");
  await page.locator("#font-cut").selectOption("compact");
  await expect(page.locator("#unsupported")).toHaveText("");
  await expect(page.locator("#glyph-summary")).toContainText("82");
  await page.locator("#font-cut").selectOption("square");
  await expect(page.locator("#font-role")).toContainText("Source-only");
});

test("weather filtering, integer scaling and transparent PNG exports", async ({ page }) => {
  await page.goto("/#icons");
  await expect(page.locator("#weather-icons .asset-card")).toHaveCount(32);
  await page.locator("#icon-search").fill("clear");
  await page.locator("#icon-phase").selectOption("night");
  await expect(page.locator("#weather-icons .asset-card")).toHaveCount(1);
  await page.locator("#icon-scale").selectOption("9");
  expect(await page.locator("#weather-icons canvas").evaluate((canvas) => canvas.width)).toBe(144);
  await page.getByRole("button", { name: "Cell grid", exact: true }).click();
  await expect(page.getByRole("button", { name: "Cell grid", exact: true })).toHaveAttribute("aria-pressed", "true");
  const download = page.waitForEvent("download");
  await page.locator("#weather-icons").getByRole("button", { name: /PNG/ }).click();
  const file = await download;
  expect(file.suggestedFilename()).toMatch(/^raster90-night-\d\d\.png$/);
  const bytes = require("node:fs").readFileSync(await file.path());
  expect(bytes.readUInt32BE(16)).toBe(48);
  expect(bytes.readUInt32BE(20)).toBe(48);
  expect(await page.evaluate(async (base64) => {
    const image = new Image(); image.src = `data:image/png;base64,${base64}`; await image.decode();
    const canvas = document.createElement("canvas"); canvas.width = 48; canvas.height = 48;
    const context = canvas.getContext("2d"); context.drawImage(image, 0, 0);
    const pixels = context.getImageData(0, 0, 48, 48).data;
    for (let y = 0; y < 48; y++) for (let x = 0; x < 48; x++) {
      if ((x >= 45 || y >= 45) && pixels[(y * 48 + x) * 4 + 3] !== 0) return false;
    }
    return true;
  }, bytes.toString("base64"))).toBe(true);
});

async function controlledClock(page) {
  await page.clock.install({ time: new Date("2026-10-07T12:00:00Z") });
  await page.clock.pauseAt(new Date("2026-10-07T12:00:01Z"));
}

const motionPixels = (page) => page.locator('#motion-icons canvas[aria-label="rain"]').evaluate((canvas) => canvas.toDataURL());

test("native browser timers visibly animate both loop and one-shot playback", async ({ page }) => {
  await page.goto("/#motion");
  const resting = await motionPixels(page);
  await expect.poll(() => motionPixels(page), { timeout: 2500 }).not.toBe(resting);
  await page.getByRole("button", { name: "Play once", exact: true }).click();
  const first = await motionPixels(page);
  await expect.poll(() => motionPixels(page), { timeout: 1500 }).not.toBe(first);
  await expect(page.getByRole("button", { name: "Play loop", exact: true })).toBeVisible({ timeout: 4000 });
  await expect(page.locator("#motion-position")).toHaveText("1 / 8");
});

test("motion loops on entry, pauses, resumes and stops when leaving", async ({ page }) => {
  await controlledClock(page);
  await page.goto("/#motion");
  await expect(page.locator("#motion-icons .asset-card")).toHaveCount(16);
  await expect(page.getByRole("button", { name: "Pause", exact: true })).toBeVisible();
  const resting = await motionPixels(page);
  await page.clock.runFor(750);
  expect(await motionPixels(page)).not.toBe(resting);
  await page.clock.runFor(1250);
  await expect(page.locator("#motion-position")).toHaveText("1 / 8");
  await page.clock.runFor(750);
  expect(await motionPixels(page)).toBe(resting);
  await page.clock.runFor(1000);
  expect(await motionPixels(page)).not.toBe(resting);
  await page.getByRole("button", { name: "Pause", exact: true }).click();
  const paused = await motionPixels(page);
  await page.clock.runFor(3000);
  expect(await motionPixels(page)).toBe(paused);
  await page.getByRole("button", { name: "Play loop", exact: true }).click();
  await page.getByRole("tab", { name: "Type", exact: true }).click();
  await page.clock.runFor(3000);
  expect(await motionPixels(page)).toBe(resting);
  await page.getByRole("tab", { name: "Motion", exact: true }).click();
  await page.clock.runFor(750);
  expect(await motionPixels(page)).not.toBe(resting);
});

test("Play once visibly advances eight phases and stays at rest afterward", async ({ page }) => {
  await controlledClock(page);
  await page.goto("/#motion");
  await page.getByRole("button", { name: "Play once", exact: true }).click();
  const phases = [];
  for (let frame = 0; frame < 8; frame++) {
    await expect(page.locator("#motion-position")).toHaveText(`${frame + 1} / 8`);
    phases.push(await motionPixels(page));
    await page.clock.runFor(250);
  }
  expect(new Set(phases).size).toBeGreaterThan(1);
  await expect(page.locator("#motion-position")).toHaveText("1 / 8");
  await expect(page.getByRole("button", { name: "Play loop", exact: true })).toBeVisible();
  await page.clock.runFor(3000);
  expect(await motionPixels(page)).toBe(phases[0]);
  await page.locator("#motion-frame").focus();
  for (let step = 0; step < 4; step++) await page.keyboard.press("ArrowRight");
  await expect(page.locator("#motion-position")).toHaveText("5 / 8");
  const first = page.locator("#motion-icons .asset-card").first();
  const cells = await first.locator("pre").textContent();
  const download = page.waitForEvent("download");
  await first.getByRole("button", { name: /matrix/ }).click();
  const matrix = JSON.parse(require("node:fs").readFileSync(await (await download).path(), "utf8"));
  expect(matrix.frame_index).toBe(4);
  expect(matrix.frame_rate).toBe(4);
  expect(matrix.rows.join("\n")).toBe(cells);
  await page.getByRole("button", { name: "Resting frame", exact: true }).click();
  expect(await motionPixels(page)).toBe(phases[0]);
});

test("reduced motion keeps previews still while permitting explicit playback", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await controlledClock(page);
  await page.goto("/#motion");
  const resting = await motionPixels(page);
  await page.clock.runFor(4000);
  expect(await motionPixels(page)).toBe(resting);
  await expect(page.getByRole("button", { name: "Play loop", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Play once", exact: true }).click();
  await page.clock.runFor(750);
  expect(await motionPixels(page)).not.toBe(resting);
  await page.clock.runFor(1250);
  expect(await motionPixels(page)).toBe(resting);
  await page.getByRole("tab", { name: "Design", exact: true }).click();
  expect(await page.locator("#hero-preview").evaluate((image) => image.currentSrc)).toMatch(/composition-466\.png$/);
  await expect(page.locator("#hero-pause")).toBeHidden();
});

test("the animated hero changes pixels and can be paused", async ({ page }) => {
  await page.goto("/#design");
  const hero = page.locator("#hero-preview");
  await hero.evaluate((image) => image.decode());
  const frames = [];
  for (let sample = 0; sample < 5; sample++) {
    frames.push((await hero.screenshot()).toString("base64"));
    await page.waitForTimeout(260);
  }
  expect(new Set(frames).size).toBeGreaterThan(1);
  await page.getByRole("button", { name: "Pause preview", exact: true }).click();
  await expect.poll(() => hero.evaluate((image) => image.currentSrc)).toMatch(/composition-466\.png$/);
  await page.getByRole("button", { name: "Play preview", exact: true }).click();
  await expect.poll(() => hero.evaluate((image) => image.currentSrc)).toMatch(/composition-466\.gif$/);
});

test("runtime examples retain dates, limits and exact hashes", async ({ page }) => {
  await page.goto("/#examples");
  await expect(page.locator(".capture-card")).toHaveCount(4);
  await expect(page.locator(".capture-card").first()).toContainText("2026-10-07");
  await expect(page.locator(".capture-card").first()).toContainText("Still capture");
  const images = page.locator(".capture-card img");
  for (const image of await images.all()) {
    await image.scrollIntoViewIfNeeded();
    await expect(image).toHaveJSProperty("complete", true);
    expect(await image.evaluate((element) => element.naturalWidth)).toBeGreaterThan(0);
  }
});

for (const width of [390, 1280]) {
  test(`all sections fit a ${width}px viewport`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    for (const name of ["Design", "Type", "Icons", "Motion", "Examples"]) {
      await page.getByRole("tab", { name, exact: true }).click();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    }
  });
}
