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

## Debug Extension

### Firefox
- **Debug URL**: `about:debugging#/runtime/this-firefox`
- Find your extension → Click **"Inspect"** 
- Opens DevTools console for background/content script logs

### Chrome  
- Go to `chrome://extensions/`
- Find your extension → Click **"Inspect views: background page"**
- Opens DevTools for background script debugging
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