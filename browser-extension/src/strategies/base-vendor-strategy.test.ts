import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { BaseVendorStrategy } from './base-vendor-strategy';

// Test implementation of abstract class
class TestVendorStrategy extends BaseVendorStrategy {
  async searchFood(foodName: string): Promise<void> {
    // Test implementation
  }
  
  async addToCart(): Promise<boolean> {
    return true;
  }
  
  getVendorId(): string {
    return 'test-vendor';
  }
}

describe('BaseVendorStrategy', () => {
  let strategy: TestVendorStrategy;
  let mockElement: HTMLElement;

  beforeEach(() => {
    strategy = new TestVendorStrategy();
    mockElement = document.createElement('div');
    
    // Reset DOM
    document.body.innerHTML = '';
  });

  afterEach(() => {
    vi.clearAllMocks();
    vi.restoreAllMocks();
  });

  describe('waitForElement', () => {
    it('should return element if it already exists', async () => {
      // Setup existing element
      mockElement.className = 'test-element';
      document.body.appendChild(mockElement);

      const result = await strategy['waitForElement']('.test-element');
      
      expect(result).toBe(mockElement);
    });

    it('should wait for element to be added to DOM', async () => {
      const elementPromise = strategy['waitForElement']('.test-element');

      // Simulate element being added after a delay
      setTimeout(() => {
        mockElement.className = 'test-element';
        document.body.appendChild(mockElement);
      }, 100);

      const result = await elementPromise;
      expect(result).toBe(mockElement);
    });

    it('should timeout if element is never found', async () => {
      await expect(
        strategy['waitForElement']('.non-existent', 100)
      ).rejects.toThrow('Element .non-existent not found within 100ms');
    });

    it('should use custom timeout', async () => {
      const startTime = Date.now();
      
      try {
        await strategy['waitForElement']('.non-existent', 200);
      } catch (error) {
        const duration = Date.now() - startTime;
        expect(duration).toBeGreaterThanOrEqual(200);
        expect(duration).toBeLessThan(300); // Allow some margin
      }
    });
  });

  describe('clickElement', () => {
    it('should click element when found', async () => {
      const clickSpy = vi.fn();
      mockElement.className = 'clickable';
      mockElement.click = clickSpy;
      document.body.appendChild(mockElement);

      await strategy['clickElement']('.clickable');
      
      expect(clickSpy).toHaveBeenCalledOnce();
    });

    it('should throw error if element is not clickable', async () => {
      // Create non-HTMLElement (like Text node)
      const textNode = document.createTextNode('text');
      vi.spyOn(document, 'querySelector').mockReturnValue(textNode as any);

      await expect(
        strategy['clickElement']('.text-node')
      ).rejects.toThrow('Element .text-node is not clickable');
    });

    it('should wait for element before clicking', async () => {
      const clickSpy = vi.fn();
      mockElement.className = 'delayed-clickable';
      mockElement.click = clickSpy;

      const clickPromise = strategy['clickElement']('.delayed-clickable');

      // Add element after a delay
      setTimeout(() => {
        document.body.appendChild(mockElement);
      }, 50);

      await clickPromise;
      expect(clickSpy).toHaveBeenCalledOnce();
    });
  });

  describe('abstract method implementation', () => {
    it('should implement all required abstract methods', () => {
      expect(strategy.searchFood).toBeDefined();
      expect(strategy.addToCart).toBeDefined();
      expect(strategy.getVendorId).toBeDefined();
      
      expect(typeof strategy.searchFood).toBe('function');
      expect(typeof strategy.addToCart).toBe('function');
      expect(typeof strategy.getVendorId).toBe('function');
    });

    it('should return vendor id', () => {
      expect(strategy.getVendorId()).toBe('test-vendor');
    });

    it('should return boolean from addToCart', async () => {
      const result = await strategy.addToCart();
      expect(typeof result).toBe('boolean');
    });
  });

  describe('MutationObserver integration', () => {
    it('should observe DOM changes when waiting for element', async () => {
      const observerSpy = vi.fn();
      const mockObserver = {
        observe: observerSpy,
        disconnect: vi.fn()
      };
      
      vi.spyOn(window, 'MutationObserver').mockImplementation((callback) => {
        // Immediately trigger the callback to simulate element appearing
        setTimeout(() => {
          mockElement.className = 'observed-element';
          document.body.appendChild(mockElement);
          callback([] as any, mockObserver as any);
        }, 10);
        
        return mockObserver as any;
      });

      const result = await strategy['waitForElement']('.observed-element');
      
      expect(observerSpy).toHaveBeenCalledWith(document.body, {
        childList: true,
        subtree: true
      });
      expect(result).toBe(mockElement);
    });
  });
});