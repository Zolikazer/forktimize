// MessageService - Simple popup ↔ content communication
export class MessageService {
  constructor(
    private browserAPI = typeof (globalThis as any).browser !== 'undefined' 
      ? (globalThis as any).browser 
      : (globalThis as any).chrome
  ) {}

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
}