// TypeScript version - for now just import the existing JS logic
import './constants';

// Import and re-export everything from the existing content.js
// This allows us to gradually migrate while keeping things working
console.log('TypeScript content script loaded! 🔥');

// For now, we'll load the old JS content script alongside
// Later we'll migrate piece by piece