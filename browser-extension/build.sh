#!/bin/bash

echo "🔨 Building TypeScript extension..."

# Clean dist directory
rm -rf dist
mkdir -p dist

# Build main files (popup, background)
echo "🔧 Building main files..."
npm run build:vite:main

# Build content script separately and ensure it doesn't overwrite
echo "🔧 Building content script..."
npm run build:vite:content

# Copy static files needed for extension
echo "📄 Copying static files..."
cp src/popup.html dist/
cp manifest-chrome.json dist/manifest-chrome.json
cp manifest-firefox.json dist/manifest-firefox.json

# Create a default manifest.json pointing to Firefox version (main platform)
cp manifest-firefox.json dist/manifest.json

echo "✅ TypeScript extension build complete in dist/"
echo "🚀 Load dist/ in your browser for testing!"