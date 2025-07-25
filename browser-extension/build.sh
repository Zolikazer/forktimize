#!/bin/bash

echo "🔨 Building cross-browser extension..."

# Clean previous builds
rm -rf dist/

# Create build directories
mkdir -p dist/chrome dist/firefox

# Copy source files to both builds
cp src/* dist/chrome/
cp src/* dist/firefox/

# Copy appropriate manifests
cp manifest-chrome.json dist/chrome/manifest.json
cp manifest-firefox.json dist/firefox/manifest.json

echo "✅ Chrome build: dist/chrome/"
echo "✅ Firefox build: dist/firefox/"
echo "🎉 Build complete!"