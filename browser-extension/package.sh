#!/bin/bash

# Package browser extension for distribution
# Creates zip files for Chrome Web Store and Firefox Add-ons

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Packaging Forktimize Browser Extension..."

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "❌ dist folder not found. Run ./build.sh first."
    exit 1
fi

# Create release directory
mkdir -p release

# Create temporary directories for each browser
TMP_DIR=$(mktemp -d)
echo "📦 Preparing browser-specific packages in $TMP_DIR..."
mkdir -p "$TMP_DIR/chrome" "$TMP_DIR/firefox"

# Copy common files to both
cp -r dist/* "$TMP_DIR/chrome/"
cp -r dist/* "$TMP_DIR/firefox/"

# Set browser-specific manifests
cp "$TMP_DIR/chrome/manifest-chrome.json" "$TMP_DIR/chrome/manifest.json"
cp "$TMP_DIR/firefox/manifest-firefox.json" "$TMP_DIR/firefox/manifest.json"

# Remove the extra manifest files
rm "$TMP_DIR/chrome/manifest-chrome.json" "$TMP_DIR/chrome/manifest-firefox.json"
rm "$TMP_DIR/firefox/manifest-chrome.json" "$TMP_DIR/firefox/manifest-firefox.json"

# Package Chrome extension
echo "📦 Creating Chrome package..."
(cd "$TMP_DIR/chrome" && zip -r "$SCRIPT_DIR/release/forktimize-extension-chrome.zip" . -x "*.map")

# Package Firefox extension
echo "📦 Creating Firefox package..."
(cd "$TMP_DIR/firefox" && zip -r "$SCRIPT_DIR/release/forktimize-extension-firefox.zip" . -x "*.map")

# Clean up temp directories
rm -rf "$TMP_DIR"

echo "✅ Extension packages created:"
echo "   📁 release/forktimize-extension-chrome.zip"
echo "   📁 release/forktimize-extension-firefox.zip"

# Show package info
echo ""
echo "📊 Package sizes:"
ls -lh release/*.zip | awk '{print "   " $9 ": " $5}'

echo ""
echo "🎉 Ready for publishing!"