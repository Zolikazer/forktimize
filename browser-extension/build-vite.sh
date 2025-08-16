#!/bin/bash

echo "🔨 Building TypeScript extension..."

# Clean dist-vite directory
rm -rf dist-vite
mkdir -p dist-vite

# Build main files (popup, background, constants)
echo "🔧 Building main files..."
npm run build:vite:main

# Build content script separately and ensure it doesn't overwrite
echo "🔧 Building content script..."
npm run build:vite:content

# Copy static files needed for extension
echo "📄 Copying static files..."
cp src/popup.html dist-vite/
cp manifest-vite-chrome.json dist-vite/manifest-chrome.json
cp manifest-vite-firefox.json dist-vite/manifest-firefox.json

# Create a default manifest.json pointing to Firefox version (main platform)
cp manifest-vite-firefox.json dist-vite/manifest.json

echo "✅ TypeScript extension build complete in dist-vite/"
echo "🚀 Load dist-vite/ in your browser for testing!"