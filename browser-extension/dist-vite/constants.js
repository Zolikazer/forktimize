const MESSAGE_TYPES = {
  EXTENSION_CHECK: "FORKTIMIZE_EXTENSION_CHECK",
  EXTENSION_PRESENT: "FORKTIMIZE_EXTENSION_PRESENT",
  MEAL_PLAN_DATA: "FORKTIMIZE_MEAL_PLAN_DATA",
  AUTO_CART: "FORKTIMIZE_AUTO_CART"
};
const UI_TEXT = {
  BUTTON_DEFAULT: "🛒 Add to Cart",
  BUTTON_PROCESSING: "⏳ Adding...",
  BUTTON_SUCCESS: "✅ Added!",
  BUTTON_FAILED: "❌ Failed"
};
const VENDOR_SITES = {
  cityfood: "rendel.cityfood.hu"
};
const CITYFOOD_SELECTORS = {
  FOOD_TITLE: ".menu-item-title",
  FOOD_CONTAINER: ".menu-item",
  CATEGORY: ".category",
  DATE_BUTTON: ".date-selector button",
  ADD_BUTTON: ".add-to-cart"
};
globalThis.FORKTIMIZE_CONSTANTS = {
  MESSAGE_TYPES,
  UI_TEXT,
  VENDOR_SITES,
  CITYFOOD_SELECTORS
};
//# sourceMappingURL=constants.js.map
