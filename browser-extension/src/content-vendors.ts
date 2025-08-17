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

  try {
    const results = await cartService.processAutoCart(data);
    const successCount = results.filter(r => r.success).length;
    const totalCount = results.length;

    if (successCount === totalCount) {
      sendResponse({
        success: true,
        message: `Successfully added all ${successCount} foods to cart!`,
        results
      });
    } else {
      sendResponse({
        success: false,
        message: `Added ${successCount}/${totalCount} foods to cart`,
        results
      });
    }
  } catch (error) {
    console.error('❌ Auto-cart failed:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    sendResponse({
      success: false,
      message: `Auto-cart failed: ${errorMessage}`,
      error: errorMessage
    });
  }
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