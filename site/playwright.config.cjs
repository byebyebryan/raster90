const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  outputDir: "../outputs/raster90/site-tests/artifacts",
  reporter: "list",
  fullyParallel: true,
  workers: process.env.CI ? 3 : undefined,
  use: { baseURL: "http://127.0.0.1:8765" },
  projects: ["chromium", "firefox", "webkit"].map((name) => ({ name, use: { browserName: name } })),
  webServer: {
    command: "python3 -m http.server 8765 --bind 127.0.0.1 --directory ../outputs/raster90/site",
    url: "http://127.0.0.1:8765",
    reuseExistingServer: false,
  },
});
