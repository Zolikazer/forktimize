// ClearButton component tests
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ClearButtonComponent } from './clear-button.component';
import { StorageService } from '../services/storage-service';

// Mock StorageService
vi.mock('../services/storage-service', () => ({
  StorageService: vi.fn()
}));

describe('ClearButtonComponent', () => {
  let component: ClearButtonComponent;
  let mockStorageService: any;

  beforeEach(() => {
    // Setup mock storage service
    mockStorageService = {
      clearAllMealPlans: vi.fn().mockResolvedValue(void 0)
    };

    // Create component
    component = new ClearButtonComponent({ storageService: mockStorageService });

    // Mock timers and confirm dialog
    vi.useFakeTimers();
    global.confirm = vi.fn().mockReturnValue(true);
    vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  describe('render', () => {
    it('should create a button with correct class and text', () => {
      const button = component.render();

      expect(button.tagName).toBe('BUTTON');
      expect(button.className).toBe('clear-btn');
      expect(button.textContent).toBe('🗑️ Clear All');
    });
  });

  describe('click handling', () => {
    it('should handle successful clear operation', async () => {
      const button = component.render() as HTMLButtonElement;
      
      // Trigger click and wait for handler to complete
      await (component as any).handleClick(button);
      
      // Should call storage service
      expect(mockStorageService.clearAllMealPlans).toHaveBeenCalled();
      
      // Should set success state
      expect(button.textContent).toBe('✅ Cleared!');
      expect(button.disabled).toBe(false);
      
      // Should reset after 2 seconds
      vi.advanceTimersByTime(2000);
      expect(button.textContent).toBe('🗑️ Clear All');
    });

    it('should handle user canceling confirmation', () => {
      global.confirm = vi.fn().mockReturnValue(false);
      const button = component.render() as HTMLButtonElement;
      
      button.click();
      
      expect(mockStorageService.clearAllMealPlans).not.toHaveBeenCalled();
      expect(button.textContent).toBe('🗑️ Clear All');
      expect(button.disabled).toBe(false);
    });

    it('should handle clear operation failure', async () => {
      mockStorageService.clearAllMealPlans.mockRejectedValue(new Error('Storage error'));
      const button = component.render() as HTMLButtonElement;
      
      // Trigger click and wait for handler to complete
      await (component as any).handleClick(button);
      
      expect(console.error).toHaveBeenCalledWith('Failed to clear meal plans:', expect.any(Error));
      expect(button.textContent).toBe('🗑️ Clear All');
      expect(button.disabled).toBe(false);
    });

    it('should show confirmation dialog with correct message', () => {
      const button = component.render() as HTMLButtonElement;
      
      button.click();
      
      expect(global.confirm).toHaveBeenCalledWith('Clear all meal plans? This cannot be undone.');
    });
  });
});