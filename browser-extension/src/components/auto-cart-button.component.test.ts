// AutoCartButton component tests
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AutoCartButtonComponent } from './auto-cart-button.component';
import type { MealPlan } from '../services/storage-service';
import * as browserMessaging from '../services/browser-messaging';

// Mock the browser messaging module
vi.mock('../services/browser-messaging', () => ({
  sendAutoCartMessage: vi.fn(),
  getCurrentTab: vi.fn()
}));

describe('AutoCartButtonComponent', () => {
  let component: AutoCartButtonComponent;
  let mockPlan: MealPlan;
  let mockTab: { id: number };

  beforeEach(() => {
    // Setup mock data
    mockPlan = {
      date: '2025-01-15',
      foodVendor: 'CityFood',
      foods: ['Chicken Rice', 'Beef Stew'],
      exportedAt: '2025-01-15T10:00:00Z',
      addedAt: '2025-01-15T10:00:00Z'
    };

    mockTab = { id: 123 };

    // Setup mocks
    vi.mocked(browserMessaging.getCurrentTab).mockResolvedValue(mockTab);
    vi.mocked(browserMessaging.sendAutoCartMessage).mockResolvedValue(undefined);

    // Create component
    component = new AutoCartButtonComponent({ plan: mockPlan });

    // Mock timers
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  describe('render', () => {
    it('should create a button with correct class and text', () => {
      const button = component.render();

      expect(button.tagName).toBe('BUTTON');
      expect(button.className).toBe('auto-cart-btn');
      expect(button.textContent).toBe('🛒 Add to Cart');
    });

    it('should add click event listener', () => {
      const button = component.render();
      const clickHandler = vi.fn();
      
      // Mock the private handleClick method
      const handleClickSpy = vi.spyOn(component as any, 'handleClick');
      
      button.click();
      
      expect(handleClickSpy).toHaveBeenCalledWith(button);
    });
  });

  describe('handleClick', () => {
    it('should handle successful auto-cart flow', async () => {
      const button = component.render() as HTMLButtonElement;
      
      // Click the button and wait for the promise to resolve
      const clickPromise = (component as any).handleClick(button);
      
      // Should set processing state immediately
      expect(button.disabled).toBe(true);
      expect(button.textContent).toBe('⏳ Adding...');
      
      // Wait for async operations to complete
      await clickPromise;
      
      // Should call messaging functions
      expect(browserMessaging.getCurrentTab).toHaveBeenCalled();
      expect(browserMessaging.sendAutoCartMessage).toHaveBeenCalledWith(123, {
        date: '2025-01-15',
        vendor: 'CityFood',
        foods: ['Chicken Rice', 'Beef Stew']
      });
      
      // Should set success state
      expect(button.textContent).toBe('✅ Added!');
    });

    it('should handle tab retrieval failure', async () => {
      vi.mocked(browserMessaging.getCurrentTab).mockResolvedValue({ id: undefined } as any);
      
      const button = component.render() as HTMLButtonElement;
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      
      await (component as any).handleClick(button);
      
      expect(button.textContent).toBe('❌ Failed');
      expect(consoleSpy).toHaveBeenCalledWith('Auto-cart failed:', expect.any(Error));
      
      consoleSpy.mockRestore();
    });

    it('should handle sendAutoCartMessage failure', async () => {
      vi.mocked(browserMessaging.sendAutoCartMessage).mockRejectedValue(new Error('Network error'));
      
      const button = component.render() as HTMLButtonElement;
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      
      await (component as any).handleClick(button);
      
      expect(button.textContent).toBe('❌ Failed');
      expect(consoleSpy).toHaveBeenCalledWith('Auto-cart failed:', expect.any(Error));
      
      consoleSpy.mockRestore();
    });

    it('should reset button state after 2 seconds on success', async () => {
      const button = component.render() as HTMLButtonElement;
      
      await (component as any).handleClick(button);
      
      // Should be in success state
      expect(button.textContent).toBe('✅ Added!');
      
      // Fast-forward 2 seconds
      vi.advanceTimersByTime(2000);
      
      // Should reset to default state
      expect(button.disabled).toBe(false);
      expect(button.textContent).toBe('🛒 Add to Cart');
    });

    it('should reset button state after 2 seconds on failure', async () => {
      vi.mocked(browserMessaging.sendAutoCartMessage).mockRejectedValue(new Error('Test error'));
      
      const button = component.render() as HTMLButtonElement;
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      
      await (component as any).handleClick(button);
      
      // Should be in failed state
      expect(button.textContent).toBe('❌ Failed');
      
      // Fast-forward 2 seconds
      vi.advanceTimersByTime(2000);
      
      // Should reset to default state
      expect(button.disabled).toBe(false);
      expect(button.textContent).toBe('🛒 Add to Cart');
      
      consoleSpy.mockRestore();
    });

    it('should log correct information on click', async () => {
      const button = component.render() as HTMLButtonElement;
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
      
      await (component as any).handleClick(button);
      
      expect(consoleSpy).toHaveBeenCalledWith('🛒 Auto-cart clicked for:', '2025-01-15', 'CityFood');
      
      consoleSpy.mockRestore();
    });
  });

  describe('setButtonState', () => {
    it('should handle PROCESSING state correctly', () => {
      const button = component.render() as HTMLButtonElement;
      
      // Access private method for testing
      (component as any).setButtonState(button, 'PROCESSING');
      
      expect(button.disabled).toBe(true);
      expect(button.textContent).toBe('⏳ Adding...');
    });

    it('should handle SUCCESS state correctly', () => {
      const button = component.render() as HTMLButtonElement;
      
      (component as any).setButtonState(button, 'SUCCESS');
      
      expect(button.disabled).toBe(false);
      expect(button.textContent).toBe('✅ Added!');
    });

    it('should handle FAILED state correctly', () => {
      const button = component.render() as HTMLButtonElement;
      
      (component as any).setButtonState(button, 'FAILED');
      
      expect(button.disabled).toBe(false);
      expect(button.textContent).toBe('❌ Failed');
    });

    it('should handle DEFAULT state correctly', () => {
      const button = component.render() as HTMLButtonElement;
      
      (component as any).setButtonState(button, 'DEFAULT');
      
      expect(button.disabled).toBe(false);
      expect(button.textContent).toBe('🛒 Add to Cart');
    });
  });
});