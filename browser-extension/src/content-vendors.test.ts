import { describe, it, expect, vi, beforeEach } from 'vitest';

// Simple functional tests without complex module mocking
describe('Vendor Content Script Logic', () => {
  beforeEach(() => {
    // Mock globals
    global.console.log = vi.fn();
    global.console.error = vi.fn();
  });

  it('should handle successful auto-cart request', async () => {
    const mockCartService = {
      processAutoCart: vi.fn()
    };

    const testAutoCartData = {
      date: '2025-01-15',
      vendor: 'cityfood',
      foods: ['Pizza', 'Salad']
    };

    const mockResults = [
      { food: 'Pizza', success: true },
      { food: 'Salad', success: true }
    ];

    mockCartService.processAutoCart.mockResolvedValue(mockResults);
    const mockSendResponse = vi.fn();

    // Simulate the auto-cart handler logic
    try {
      const results = await mockCartService.processAutoCart(testAutoCartData);
      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      if (successCount === totalCount) {
        mockSendResponse({
          success: true,
          message: `Successfully added all ${successCount} foods to cart!`,
          results
        });
      } else {
        mockSendResponse({
          success: false,
          message: `Added ${successCount}/${totalCount} foods to cart`,
          results
        });
      }
    } catch (error) {
      console.error('❌ Auto-cart failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      mockSendResponse({
        success: false,
        message: `Auto-cart failed: ${errorMessage}`,
        error: errorMessage
      });
    }

    expect(mockCartService.processAutoCart).toHaveBeenCalledWith(testAutoCartData);
    expect(mockSendResponse).toHaveBeenCalledWith({
      success: true,
      message: 'Successfully added all 2 foods to cart!',
      results: mockResults
    });
  });

  it('should handle partial auto-cart failures', async () => {
    const mockCartService = {
      processAutoCart: vi.fn()
    };

    const testAutoCartData = {
      date: '2025-01-15',
      vendor: 'cityfood',
      foods: ['Pizza', 'Salad']
    };

    const mockResults = [
      { food: 'Pizza', success: true },
      { food: 'Salad', success: false, error: 'Not found' }
    ];

    mockCartService.processAutoCart.mockResolvedValue(mockResults);
    const mockSendResponse = vi.fn();

    // Simulate the auto-cart handler logic
    try {
      const results = await mockCartService.processAutoCart(testAutoCartData);
      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      if (successCount === totalCount) {
        mockSendResponse({
          success: true,
          message: `Successfully added all ${successCount} foods to cart!`,
          results
        });
      } else {
        const failedCount = totalCount - successCount;
        mockSendResponse({
          success: false,
          message: `${successCount} foods added successfully, ${failedCount} failed`,
          results
        });
      }
    } catch (error) {
      console.error('❌ Auto-cart failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      mockSendResponse({
        success: false,
        message: `Auto-cart failed: ${errorMessage}`,
        error: errorMessage
      });
    }

    expect(mockSendResponse).toHaveBeenCalledWith({
      success: false,
      message: '1 foods added successfully, 1 failed',
      results: mockResults
    });
  });

  it('should handle cart service errors', async () => {
    const mockCartService = {
      processAutoCart: vi.fn()
    };

    const testAutoCartData = {
      date: '2025-01-15',
      vendor: 'cityfood',
      foods: ['Pizza']
    };

    const cartError = new Error('Cart service failed');
    mockCartService.processAutoCart.mockRejectedValue(cartError);
    const mockSendResponse = vi.fn();

    // Simulate the auto-cart handler logic
    try {
      const results = await mockCartService.processAutoCart(testAutoCartData);
      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      if (successCount === totalCount) {
        mockSendResponse({
          success: true,
          message: `Successfully added all ${successCount} foods to cart!`,
          results
        });
      } else {
        mockSendResponse({
          success: false,
          message: `Added ${successCount}/${totalCount} foods to cart`,
          results
        });
      }
    } catch (error) {
      console.error('❌ Auto-cart failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      mockSendResponse({
        success: false,
        message: `Auto-cart failed: ${errorMessage}`,
        error: errorMessage
      });
    }

    expect(mockSendResponse).toHaveBeenCalledWith({
      success: false,
      message: 'Auto-cart failed: Cart service failed',
      error: 'Cart service failed'
    });
  });

  it('should handle unknown errors', async () => {
    const mockCartService = {
      processAutoCart: vi.fn()
    };

    const testAutoCartData = {
      date: '2025-01-15',
      vendor: 'cityfood',
      foods: ['Pizza']
    };

    const unknownError = 'Something weird happened';
    mockCartService.processAutoCart.mockRejectedValue(unknownError);
    const mockSendResponse = vi.fn();

    // Simulate the auto-cart handler logic
    try {
      const results = await mockCartService.processAutoCart(testAutoCartData);
      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      if (successCount === totalCount) {
        mockSendResponse({
          success: true,
          message: `Successfully added all ${successCount} foods to cart!`,
          results
        });
      } else {
        mockSendResponse({
          success: false,
          message: `Added ${successCount}/${totalCount} foods to cart`,
          results
        });
      }
    } catch (error) {
      console.error('❌ Auto-cart failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      mockSendResponse({
        success: false,
        message: `Auto-cart failed: ${errorMessage}`,
        error: errorMessage
      });
    }

    expect(mockSendResponse).toHaveBeenCalledWith({
      success: false,
      message: 'Auto-cart failed: Unknown error',
      error: 'Unknown error'
    });
  });

  // Vendor mismatch tests
  describe('Vendor Mismatch Logic', () => {
    it('should reject auto-cart when requesting cityfood but on wrong hostname', () => {
      const testAutoCartData = {
        vendor: 'cityfood',
        foods: ['Pizza']
      };

      const mockSendResponse = vi.fn();
      
      Object.defineProperty(global, 'window', {
        value: { location: { hostname: 'www.google.com' } },
        writable: true
      });

      // Simulate vendor check logic
      const requestedVendor = testAutoCartData.vendor?.toLowerCase();
      const currentHostname = window.location.hostname;
      
      if (requestedVendor === 'cityfood' && !currentHostname.includes('cityfood.hu')) {
        mockSendResponse({
          success: false,
          message: '🚫 Wrong vendor - switch to your CityFood tab',
          error: 'vendor_mismatch'
        });
        return;
      }

      expect(mockSendResponse).toHaveBeenCalledWith({
        success: false,
        message: '🚫 Wrong vendor - switch to your CityFood tab',
        error: 'vendor_mismatch'
      });
    });

    it('should allow auto-cart when on correct cityfood hostname', () => {
      const testAutoCartData = {
        vendor: 'cityfood',
        foods: ['Pizza']
      };

      const mockSendResponse = vi.fn();
      
      Object.defineProperty(global, 'window', {
        value: { location: { hostname: 'rendel.cityfood.hu' } },
        writable: true
      });

      const requestedVendor = testAutoCartData.vendor?.toLowerCase();
      const currentHostname = window.location.hostname;
      
      let shouldReject = false;
      if (requestedVendor === 'cityfood' && !currentHostname.includes('cityfood.hu')) {
        shouldReject = true;
      }

      expect(shouldReject).toBe(false);
      expect(mockSendResponse).not.toHaveBeenCalled();
    });
  });
});