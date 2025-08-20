import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  sendAutoCartMessage,
  getCurrentTab,
  onExtensionSyn,
  onMealPlanData,
  sendExtensionAck,
  onAutoCart
} from './messaging';

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

describe('Message Service Functions', () => {
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

      await sendAutoCartMessage(tabId, data, mockBrowserAPI as any);

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

      const result = await getCurrentTab(mockBrowserAPI as any);

      expect(result).toBe(mockTab);
      expect(mockBrowserAPI.tabs.query).toHaveBeenCalledWith({
        active: true,
        currentWindow: true
      });
    });
  });

  describe('onExtensionSyn', () => {
    it('should listen for SYN messages and call callback with vendor', () => {
      const callback = vi.fn();
      onExtensionSyn(callback);

      expect(window.addEventListener).toHaveBeenCalledWith('message', expect.any(Function));

      // Simulate SYN message with vendor
      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ 
        data: { 
          type: 'FORKTIMIZE_HANDSHAKE_SYN', 
          vendor: 'cityfood' 
        } 
      });

      expect(callback).toHaveBeenCalledWith('cityfood');
    });

    it('should call callback with undefined when no vendor provided', () => {
      const callback = vi.fn();
      onExtensionSyn(callback);

      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ data: { type: 'FORKTIMIZE_HANDSHAKE_SYN' } });

      expect(callback).toHaveBeenCalledWith(undefined);
    });

    it('should not call callback for other message types', () => {
      const callback = vi.fn();
      onExtensionSyn(callback);

      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ data: { type: 'OTHER_MESSAGE' } });

      expect(callback).not.toHaveBeenCalled();
    });
  });

  describe('onMealPlanData', () => {
    it('should listen for meal plan data and call callback with data', () => {
      const callback = vi.fn();
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      onMealPlanData(callback);

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

    it('should not call callback for other message types', () => {
      const callback = vi.fn();
      onMealPlanData(callback);

      const messageListener = (window.addEventListener as any).mock.calls[0][1];
      messageListener({ data: { type: 'OTHER_MESSAGE' } });

      expect(callback).not.toHaveBeenCalled();
    });
  });

  describe('sendExtensionAck', () => {
    it('should send ACK message with vendor support status', () => {
      sendExtensionAck(true);

      expect(window.postMessage).toHaveBeenCalledWith(
        { 
          type: 'FORKTIMIZE_HANDSHAKE_ACK', 
          vendorSupported: true 
        },
        '*'
      );
    });

    it('should send ACK message with vendor not supported', () => {
      sendExtensionAck(false);

      expect(window.postMessage).toHaveBeenCalledWith(
        { 
          type: 'FORKTIMIZE_HANDSHAKE_ACK', 
          vendorSupported: false 
        },
        '*'
      );
    });
  });

  describe('onAutoCart', () => {
    it('should listen for auto-cart messages and call callback with sendResponse', () => {
      const callback = vi.fn();
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      const sendResponse = vi.fn();

      onAutoCart(callback, mockBrowserAPI as any);

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

    it('should not call callback for other message types', () => {
      const callback = vi.fn();
      const sendResponse = vi.fn();

      onAutoCart(callback, mockBrowserAPI as any);

      const runtimeListener = mockBrowserAPI.runtime.onMessage.addListener.mock.calls[0][0];
      const result = runtimeListener(
        { type: 'OTHER_MESSAGE', data: {} },
        {},
        sendResponse
      );

      expect(callback).not.toHaveBeenCalled();
      expect(result).toBeUndefined(); // Should not return true for non-matching messages
    });
  });
});
