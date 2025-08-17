import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PopupService } from './popup-service';

// Mock AutoCartButton component
vi.mock('../components/auto-cart-button.component', () => ({
  AutoCartButtonComponent: vi.fn().mockImplementation(() => ({
    render: vi.fn().mockReturnValue(document.createElement('button'))
  }))
}));

// Mock message functions (not needed anymore but keeping for compatibility)
vi.mock('./browser-messaging', () => ({
  getCurrentTab: vi.fn(),
  sendAutoCartMessage: vi.fn()
}));

// Mock services
const mockStorageService = {
  loadAllMealPlans: vi.fn(),
  onStorageChange: vi.fn()
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
      const mockAutoCartSection = {
        appendChild: vi.fn()
      };
      const mockCard = {
        className: '',
        innerHTML: '',
        querySelector: vi.fn().mockReturnValue(mockAutoCartSection)
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
      expect(mockAutoCartSection.appendChild).toHaveBeenCalled(); // AutoCartButton should be appended
    });
  });

  describe('AutoCartButton integration', () => {
    it('should create and mount AutoCartButton component in day cards', async () => {
      const { AutoCartButtonComponent } = await import('../components/auto-cart-button.component');
      
      // Mock container and card elements
      const mockContainer = {
        appendChild: vi.fn(),
        innerHTML: ''
      };
      const mockCard = {
        className: '',
        innerHTML: '',
        querySelector: vi.fn().mockReturnValue({
          appendChild: vi.fn()
        })
      };

      mockDocument.getElementById.mockReturnValue(mockContainer);
      mockDocument.createElement.mockReturnValue(mockCard);

      const mealPlans = {
        '2025-01-15': {
          date: '2025-01-15',
          foodVendor: 'CityFood',
          foods: ['Pizza'],
          exportedAt: '2025-01-15T10:00:00Z',
          addedAt: '2025-01-15T10:00:00Z'
        }
      };
      mockStorageService.loadAllMealPlans.mockResolvedValue(mealPlans);

      await popupService.initialize();

      // Should create AutoCartButton component
      expect(AutoCartButtonComponent).toHaveBeenCalledWith({
        plan: mealPlans['2025-01-15']
      });
      
      // Should call render on the component
      const componentInstance = (AutoCartButtonComponent as any).mock.results[0].value;
      expect(componentInstance.render).toHaveBeenCalled();
    });
  });
});
