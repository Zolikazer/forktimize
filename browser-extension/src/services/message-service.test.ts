import { describe, it, expect, beforeEach, vi } from 'vitest';
import { MessageService } from './message-service';

const mockBrowserAPI = {
  tabs: {
    sendMessage: vi.fn(),
    query: vi.fn()
  },
  runtime: {
    onMessage: {
      addListener: vi.fn()
    }
  }
};

describe('MessageService', () => {
  let messageService: MessageService;

  beforeEach(() => {
    vi.clearAllMocks();
    // Mock window object for DOM-related tests
    Object.defineProperty(global, 'window', {
      value: {
        addEventListener: vi.fn(),
        postMessage: vi.fn()
      },
      writable: true,
      configurable: true
    });
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

  describe('onExtensionSyn', () => {
    it('should listen for SYN messages and call callback', () => {
      const callback = vi.fn();
      messageService.onExtensionSyn(callback);

      expect(window.addEventListener).toHaveBeenCalledWith('message', expect.any(Function));

      // Simulate SYN message
      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ data: { type: 'FORKTIMIZE_HANDSHAKE_SYN' } });

      expect(callback).toHaveBeenCalled();
    });

    it('should not call callback for other message types', () => {
      const callback = vi.fn();
      messageService.onExtensionSyn(callback);

      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ data: { type: 'OTHER_MESSAGE' } });

      expect(callback).not.toHaveBeenCalled();
    });
  });

  describe('onMealPlanData', () => {
    it('should listen for meal plan data and call callback with data', () => {
      const callback = vi.fn();
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      messageService.onMealPlanData(callback);

      expect(window.addEventListener).toHaveBeenCalledWith('message', expect.any(Function));

      // Simulate meal plan message
      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ 
        data: { 
          type: 'FORKTIMIZE_MEAL_PLAN_DATA', 
          data: testData 
        } 
      });

      expect(callback).toHaveBeenCalledWith(testData);
    });
  });

  describe('onAutoCart', () => {
    it('should listen for auto-cart messages and call callback', () => {
      const callback = vi.fn();
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      const sendResponse = vi.fn();
      
      messageService.onAutoCart(callback);

      expect(mockBrowserAPI.runtime.onMessage.addListener).toHaveBeenCalledWith(expect.any(Function));

      // Simulate auto-cart message
      const runtimeListener = mockBrowserAPI.runtime.onMessage.addListener.mock.calls[0][0];
      const result = runtimeListener(
        { type: 'FORKTIMIZE_AUTO_CART', data: testData },
        {},
        sendResponse
      );

      expect(callback).toHaveBeenCalledWith(testData, sendResponse);
      expect(result).toBe(true); // Should return true for async response
    });
  });

  describe('sendExtensionAck', () => {
    it('should send ACK message via postMessage', () => {
      messageService.sendExtensionAck();

      expect(window.postMessage).toHaveBeenCalledWith(
        { type: 'FORKTIMIZE_HANDSHAKE_ACK' },
        '*'
      );
    });
  });
});