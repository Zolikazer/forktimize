// Forktimize Browser Extension Constants
// Centralized configuration and message types

// Make constants available globally for browser extension context
window.FORKTIMIZE_CONSTANTS = {
  MESSAGE_TYPES: {
    // Frontend ↔ Content Script communication (via postMessage)
    EXTENSION_CHECK: 'FORKTIMIZE_EXTENSION_CHECK',
    EXTENSION_PRESENT: 'FORKTIMIZE_EXTENSION_PRESENT', 
    MEAL_PLAN_DATA: 'FORKTIMIZE_MEAL_PLAN_DATA',
    
    // Popup ↔ Content Script communication (via browser runtime)
    AUTO_CART: 'FORKTIMIZE_AUTO_CART'
  },

  VENDORS: {
    CITYFOOD: 'cityfood',
    INTERFOOD: 'interfood'
  },

  VENDOR_SITES: {
    cityfood: 'rendel.cityfood.hu',
    interfood: 'rendel.interfood.hu'
  },

  AUTO_CART_CONFIG: {
    // Delay between processing multiple foods (ms)
    FOOD_PROCESSING_DELAY: 500,
    
    // UI feedback timeout (ms) 
    FEEDBACK_DISPLAY_DURATION: 2000
  },

  CITYFOOD_SELECTORS: {
    FOOD_TITLE: '.food-top-title',
    FOOD_CONTAINER: '.food',
    CATEGORY: '.category', 
    DATE_BUTTON: '.date-button',
    ADD_BUTTON: 'button[aria-label*="Kosárhoz adás:"]'
  },

  UI_TEXT: {
    BUTTON_DEFAULT: '🛒 Auto-Add to Cart',
    BUTTON_PROCESSING: '🔄 Processing...',
    BUTTON_SUCCESS: '✅ Added to Cart!',
    BUTTON_FAILED: '❌ Failed'
  }
};