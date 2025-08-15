# Forktimize Browser Extension - Claude Context

## Overview
Cross-platform browser extension (Chrome/Firefox) that integrates with the main Forktimize web app for meal planning workflow optimization.

## Current Implementation Status

### ✅ Completed Features
- **Multi-day storage**: Extension stores meal plans by date instead of overriding
- **Cross-browser compatibility**: Works on both Chrome and Firefox
- **Frontend integration**: "Send to Extension 📱" button in MealPlan component
- **Clean popup UI**: Displays meal plans organized by day with proper formatting
- **Real-time updates**: Popup refreshes automatically when new plans are added
- **Data structure handling**: Properly extracts food names and vendor info from frontend data

### 🚧 Current Architecture

**Data Flow:**
1. Frontend detects extension presence via `FORKTIMIZE_EXTENSION_CHECK` message
2. User generates meal plan and clicks "Send to Extension 📱" 
3. Extension receives `FORKTIMIZE_MEAL_PLAN_DATA` with: `{date, foodVendor, foods[], exportedAt}`
4. Extension stores plans in `forktimizeMealPlans` object keyed by date
5. Popup displays all stored plans sorted chronologically

**File Structure:**
```
browser-extension/
├── src/
│   ├── content.js      # Message handling & storage logic
│   ├── popup.html      # Extension popup interface
│   ├── popup.js        # Popup data loading & display
│   └── background.js   # Service worker (minimal)
├── manifest-chrome.json
├── manifest-firefox.json
├── build.sh           # Cross-browser build script
└── dist/              # Built extension files (gitignored)
```

## Next Phase: Auto-Cart Integration

### 🎯 Planned Features
1. **Vendor site detection**: Recognize food vendor websites 
2. **Cart automation**: Auto-add meal plan items to vendor shopping carts
3. **Multi-vendor support**: Handle different cart systems/APIs
4. **Error handling**: Graceful failures with user feedback

### 🛠️ Development Commands
```bash
# Build extension
./build.sh

# Test in browsers
# Chrome: Load unpacked from dist/chrome/
# Firefox: Load temporary add-on from dist/firefox/manifest.json
```

### 📊 Current Todo Status
- [x] Multi-day storage implementation
- [x] Better popup UI with day organization  
- [x] Frontend integration button
- [x] Test multi-day meal plan storage
- [ ] Research food vendor cart structures
- [ ] Design auto-cart functionality
- [ ] Implement vendor-specific automation
- [ ] Add error handling for cart operations
- [ ] End-to-end flow testing

## Technical Notes
- Uses WebExtensions API for cross-browser compatibility
- Storage via `browser.storage.local` API
- Real-time UI updates via storage change listeners
- Minimal build system - no complex bundlers needed
- Follows defensive coding practices for unknown data structures