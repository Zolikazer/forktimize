// Content script for vendor domains - handles auto-cart functionality
import { CartService } from './services/cart-service';
import { DomService } from './services/dom-service';
import { StorageService } from './services/storage-service';
import { onAutoCart } from './lib/messaging';

// Inline constants for content script (matching working content-main.ts)
const CITYFOOD_SELECTORS = {
  FOOD_TITLE: '.food-top-title',
  FOOD_CONTAINER: '.food',
  CATEGORY: '.category',
  DATE_BUTTON: '.date-button',
  ADD_BUTTON: 'button[aria-label*="Kosárhoz adás:"]'
} as const;

const VENDOR_SITES = {
  cityfood: 'rendel.cityfood.hu'
} as const;

console.log('TypeScript vendor content script loaded on:', window.location.hostname);

// Create service instances with proper dependencies (from content-main.ts)
const storageService = new StorageService();
const domService = new DomService(CITYFOOD_SELECTORS);
const cartService = new CartService(
  domService, 
  storageService, 
  {
    hostname: VENDOR_SITES.cityfood,
    selectors: CITYFOOD_SELECTORS,
    name: 'CityFood'
  }
);

// Auto-cart handler function (extracted from original orchestrator)
async function handleAutoCart(data: any, sendResponse: (response: any) => void) {
  console.log('🛒 Auto-cart request received:', data);

  if (!isValidVendorForCurrentSite(data.vendor)) {
    sendVendorMismatchResponse(sendResponse);
    return;
  }

  try {
    const results = await cartService.processAutoCart(data);
    sendAutoCartResults(results, sendResponse);
  } catch (error) {
    sendAutoCartError(error, sendResponse);
  }
}

function isValidVendorForCurrentSite(vendor: string): boolean {
  const requestedVendor = vendor?.toLowerCase();
  const currentHostname = window.location.hostname;
  
  if (requestedVendor === 'cityfood') {
    return currentHostname.includes('cityfood.hu');
  }
  
  // Add more vendor checks here as we expand
  return false;
}

function sendVendorMismatchResponse(sendResponse: (response: any) => void): void {
  sendResponse({
    success: false,
    message: '🚫 Wrong vendor - switch to your CityFood tab',
    error: 'vendor_mismatch'
  });
}

function sendAutoCartResults(results: any[], sendResponse: (response: any) => void): void {
  const successCount = results.filter(r => r.success).length;
  const totalCount = results.length;

  if (successCount === totalCount) {
    sendResponse({
      success: true,
      message: `Successfully added all ${successCount} foods to cart!`,
      results
    });
  } else {
    const failedCount = totalCount - successCount;
    sendResponse({
      success: false,
      message: `${successCount} foods added successfully, ${failedCount} failed`,
      results
    });
  }
}

function sendAutoCartError(error: unknown, sendResponse: (response: any) => void): void {
  console.error('❌ Auto-cart failed:', error);
  const errorMessage = error instanceof Error ? error.message : 'Unknown error';
  sendResponse({
    success: false,
    message: `Auto-cart failed: ${errorMessage}`,
    error: errorMessage
  });
}

// Setup auto-cart handler
function setupAutoCartHandler() {
  onAutoCart(async (data, sendResponse) => {
    await handleAutoCart(data, sendResponse);
  });
}

// Initialize vendor content script
setupAutoCartHandler();

console.log('🚀 Vendor content script initialized');