import { describe, it, expect, beforeEach, vi } from 'vitest';
import { MessageService } from './message-service';

const mockBrowserAPI = {
  tabs: {
    sendMessage: vi.fn(),
    query: vi.fn()
  }
};

describe('MessageService', () => {
  let messageService: MessageService;

  beforeEach(() => {
    vi.clearAllMocks();
    messageService = new MessageService(mockBrowserAPI as any);
  });

  describe('sendAutoCartMessage', () => {
    it('should send auto-cart message to tab', async () => {
      const tabId = 123;
      const data = {
        date: '2025-01-15',
        vendor: 'CityFood',
        foods: ['Pizza', 'Salad']
      };

      mockBrowserAPI.tabs.sendMessage.mockResolvedValue({ success: true });

      await messageService.sendAutoCartMessage(tabId, data);

      expect(mockBrowserAPI.tabs.sendMessage).toHaveBeenCalledWith(tabId, {
        type: 'FORKTIMIZE_AUTO_CART',
        data
      });
    });
  });

  describe('getCurrentTab', () => {
    it('should return current active tab', async () => {
      const mockTab = { id: 123, url: 'https://rendel.cityfood.hu' };
      mockBrowserAPI.tabs.query.mockResolvedValue([mockTab]);

      const result = await messageService.getCurrentTab();

      expect(result).toBe(mockTab);
      expect(mockBrowserAPI.tabs.query).toHaveBeenCalledWith({ 
        active: true, 
        currentWindow: true 
      });
    });
  });
});