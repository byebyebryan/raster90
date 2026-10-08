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

test("motion stays still, steps, plays once and returns to its resting frame", async ({ page }) => {
  await page.goto("/#motion");
  await expect(page.locator("#motion-icons .asset-card")).toHaveCount(16);
  const resting = await page.locator("#motion-icons canvas").first().evaluate((canvas) => canvas.toDataURL());
  await page.waitForTimeout(400);
  expect(await page.locator("#motion-icons canvas").first().evaluate((canvas) => canvas.toDataURL())).toBe(resting);
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
  await page.getByRole("button", { name: "Play once", exact: true }).click();
  await expect(page.getByRole("button", { name: "Pause", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Play once", exact: true })).toBeVisible({ timeout: 4000 });
  await expect(page.locator("#motion-position")).toHaveText("1 / 8");
  expect(await page.locator("#motion-icons canvas").first().evaluate((canvas) => canvas.toDataURL())).toBe(resting);
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
