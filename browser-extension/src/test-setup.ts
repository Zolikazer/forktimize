// Simple test to verify our TypeScript setup works
console.log('TypeScript setup is working! 🔥');

// Test browser API types - using any for now since we're in transition
const browserAPI = typeof (globalThis as any).browser !== 'undefined' 
  ? (globalThis as any).browser 
  : (globalThis as any).chrome;

export const testSetup = {
  checkBrowserAPI(): boolean {
    return !!browserAPI?.storage?.local;
  },
  
  logMessage(message: string): void {
    console.log(`[Test]: ${message}`);
  }
};