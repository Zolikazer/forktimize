// MessageService - Smart message dispatcher with specific subscriptions
export class MessageService {
  constructor(
    private browserAPI = typeof (globalThis as any).browser !== 'undefined' 
      ? (globalThis as any).browser 
      : (globalThis as any).chrome
  ) {}

  // Popup → Content communication (existing)
  async sendAutoCartMessage(tabId: number, data: {
    date: string;
    vendor: string;
    foods: Array<string | { name: string }>;
  }) {
    return this.browserAPI.tabs.sendMessage(tabId, {
      type: 'FORKTIMIZE_AUTO_CART',
      data
    });
  }

  async getCurrentTab() {
    const [tab] = await this.browserAPI.tabs.query({ active: true, currentWindow: true });
    return tab;
  }

  // Specific message subscriptions (new)
  onExtensionSyn(callback: () => void) {
    window.addEventListener('message', (event) => {
      if (event.data.type === 'FORKTIMIZE_HANDSHAKE_SYN') {
        callback();
      }
    });
  }

  onMealPlanData(callback: (data: any) => void) {
    window.addEventListener('message', (event) => {
      if (event.data.type === 'FORKTIMIZE_MEAL_PLAN_DATA') {
        callback(event.data.data);
      }
    });
  }

  onAutoCart(callback: (data: any, sendResponse: (response: any) => void) => void) {
    this.browserAPI.runtime.onMessage.addListener((message: any, sender: any, sendResponse: (response: any) => void) => {
      if (message.type === 'FORKTIMIZE_AUTO_CART') {
        callback(message.data, sendResponse);
        return true; // Async response
      }
    });
  }

  // Response helpers
  sendExtensionAck() {
    window.postMessage({ type: 'FORKTIMIZE_HANDSHAKE_ACK' }, '*');
  }
}