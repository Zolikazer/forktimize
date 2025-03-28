import { defineConfig, test } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run build && npm run preview',
    port: 4173
  },
  use: {
    screenshot: "only-on-failure", // ✅ Automatically takes a screenshot on failure
    trace: "on-first-retry", // ✅ Enables tracing for failed tests
    video: "on",
    viewport: { width: 1280, height: 1600 }
  },

  testDir: 'e2e'
});


