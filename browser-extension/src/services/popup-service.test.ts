import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PopupService } from './popup-service';

// Mock services
const mockStorageService = {
  loadAllMealPlans: vi.fn(),
  onStorageChange: vi.fn()
};

const mockMessageService = {
  getCurrentTab: vi.fn(),
  sendAutoCartMessage: vi.fn()
};

// Mock DOM
const createMockDocument = () => ({
  getElementById: vi.fn(),
  createElement: vi.fn(() => ({
    className: '',
    innerHTML: '',
    appendChild: vi.fn(),
    querySelector: vi.fn(),
    addEventListener: vi.fn(),
    getAttribute: vi.fn(),
    textContent: ''
  }))
});

describe('PopupService', () => {
  let popupService: PopupService;
  let mockDocument: any;

  beforeEach(() => {
    vi.clearAllMocks();
    mockDocument = createMockDocument();
    popupService = new PopupService(
      mockStorageService as any,
      mockMessageService as any,
      mockDocument as any
    );
  });

  describe('initialize', () => {
    it('should load meal plans and setup storage listener', async () => {
      mockStorageService.loadAllMealPlans.mockResolvedValue({});

      await popupService.initialize();

      expect(mockStorageService.loadAllMealPlans).toHaveBeenCalled();
      expect(mockStorageService.onStorageChange).toHaveBeenCalled();
    });
  });

  describe('displayMealPlans', () => {
    it('should handle empty meal plans', async () => {
      const mockContainer = { innerHTML: '' };
      mockDocument.getElementById.mockReturnValue(mockContainer);
      mockStorageService.loadAllMealPlans.mockResolvedValue({});

      await popupService.initialize();

      expect(mockDocument.getElementById).toHaveBeenCalledWith('meal-plans-container');
    });

    it('should create cards for meal plans', async () => {
      const mockContainer = { 
        innerHTML: '',
        appendChild: vi.fn()
      };
      const mockCard = {
        className: '',
        innerHTML: '',
        querySelector: vi.fn().mockReturnValue({
          addEventListener: vi.fn(),
          getAttribute: vi.fn()
        })
      };

      mockDocument.getElementById.mockReturnValue(mockContainer);
      mockDocument.createElement.mockReturnValue(mockCard);

      const mealPlans = {
        '2025-01-15': {
          foodVendor: 'CityFood',
          foods: ['Pizza']
        }
      };
      mockStorageService.loadAllMealPlans.mockResolvedValue(mealPlans);

      await popupService.initialize();

      expect(mockContainer.appendChild).toHaveBeenCalled();
      expect(mockCard.className).toBe('day-plan');
    });
  });

  describe('handleAutoCartClick', () => {
    it('should send auto-cart message successfully', async () => {
      const mockButton = {
        getAttribute: vi.fn(),
        disabled: false,
        textContent: ''
      };
      
      mockButton.getAttribute
        .mockReturnValueOnce('2025-01-15') // date
        .mockReturnValueOnce('CityFood');  // vendor

      const mockTab = { id: 123 };
      mockMessageService.getCurrentTab.mockResolvedValue(mockTab);
      mockMessageService.sendAutoCartMessage.mockResolvedValue(undefined);

      const plan = { foods: ['Pizza'] };

      // Call private method via any cast for testing
      await (popupService as any).handleAutoCartClick(mockButton, plan);

      expect(mockMessageService.sendAutoCartMessage).toHaveBeenCalledWith(123, {
        date: '2025-01-15',
        vendor: 'CityFood',
        foods: ['Pizza']
      });
    });

    it('should handle auto-cart failure', async () => {
      const mockButton = {
        getAttribute: vi.fn(),
        disabled: false,
        textContent: ''
      };
      
      mockButton.getAttribute
        .mockReturnValueOnce('2025-01-15')
        .mockReturnValueOnce('CityFood');

      mockMessageService.getCurrentTab.mockRejectedValue(new Error('Tab error'));

      const plan = { foods: ['Pizza'] };

      await (popupService as any).handleAutoCartClick(mockButton, plan);

      // Should set button to failed state
      expect(mockButton.textContent).toBe('❌ Failed');
    });
  });
});