# Forktimize Browser Extension

Minimal cross-browser "Hello World" extension.

## Build & Test

```bash
# Build for both browsers
npm run build

# Test in Firefox
npm run dev:firefox

# Test in Chrome
# 1. Open Chrome -> Extensions -> Developer mode
# 2. Load unpacked -> select dist/chrome/
```

## Structure

```
browser-extension/
├── src/
│   ├── popup.html      # Extension popup
│   ├── popup.js        # Popup logic
│   ├── content.js      # Content script
│   └── background.js   # Background script
├── manifest-chrome.json # Chrome manifest
├── manifest-firefox.json # Firefox manifest
└── build.sh           # Build script
```