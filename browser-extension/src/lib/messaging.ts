// Message utilities - Pure functions for browser extension messaging

// Browser API helper
function getBrowserAPI() {
  return typeof (globalThis as any).browser !== 'undefined' 
    ? (globalThis as any).browser 
    : (globalThis as any).chrome;
}

// Popup → Content communication
export async function sendAutoCartMessage(
  tabId: number, 
  data: {
    date: string;
    vendor: string;
    foods: Array<string | { name: string }>;
  },
  browserAPI = getBrowserAPI()
) {
  return browserAPI.tabs.sendMessage(tabId, {
    type: 'FORKTIMIZE_AUTO_CART',
    data
  });
}

export async function getCurrentTab(browserAPI = getBrowserAPI()) {
  const [tab] = await browserAPI.tabs.query({ active: true, currentWindow: true });
  return tab;
}

// Frontend ↔ Content messaging (window.postMessage)
export function onExtensionSyn(callback: (vendor?: string) => void) {
  window.addEventListener('message', (event) => {
    if (event.data.type === 'FORKTIMIZE_HANDSHAKE_SYN') {
      callback(event.data.vendor);
    }
  });
}

export function onMealPlanData(callback: (data: any) => void) {
  window.addEventListener('message', (event) => {
    if (event.data.type === 'FORKTIMIZE_MEAL_PLAN_DATA') {
      callback(event.data.data);
    }
  });
}

export function sendExtensionAck(vendorSupported: boolean) {
  window.postMessage({ 
    type: 'FORKTIMIZE_HANDSHAKE_ACK', 
    vendorSupported 
  }, '*');
}

// Popup ↔ Content messaging (runtime.onMessage)
export function onAutoCart(
  callback: (data: any, sendResponse: (response: any) => void) => void,
  browserAPI = getBrowserAPI()
) {
  browserAPI.runtime.onMessage.addListener((message: any, sender: any, sendResponse: (response: any) => void) => {
    if (message.type === 'FORKTIMIZE_AUTO_CART') {
      callback(message.data, sendResponse);
      return true; // Async response
    }
  });
}