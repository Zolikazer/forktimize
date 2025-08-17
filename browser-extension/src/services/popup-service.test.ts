import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PopupService } from './popup-service';

// Mock MealPlansContainer component
vi.mock('../components/meal-plans-container.component', () => ({
  MealPlansContainerComponent: vi.fn().mockImplementation(() => ({
    render: vi.fn().mockReturnValue(() => {
      const container = document.createElement('div');
      container.id = 'meal-plans-container';
      return container;
    })()
  }))
}));

// Mock AutoCartButton component (for legacy test compatibility)
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
    it('should handle empty meal plans using MealPlansContainer', async () => {
      const { MealPlansContainerComponent } = await import('../components/meal-plans-container.component');
      
      // Mock document.body for appendChild
      const mockBody = {
        appendChild: vi.fn()
      };
      mockDocument.body = mockBody as any;
      mockDocument.getElementById.mockReturnValue(null); // No existing container

      mockStorageService.loadAllMealPlans.mockResolvedValue({});

      await popupService.initialize();

      // Should create MealPlansContainer component with empty data
      expect(MealPlansContainerComponent).toHaveBeenCalledWith({ mealPlans: {} });
      expect(mockBody.appendChild).toHaveBeenCalled();
    });

    it('should create meal plans using MealPlansContainer component', async () => {
      const { MealPlansContainerComponent } = await import('../components/meal-plans-container.component');
      
      const mockBody = {
        appendChild: vi.fn()
      };
      mockDocument.body = mockBody as any;
      mockDocument.getElementById.mockReturnValue(null);

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

      // Should create MealPlansContainer component with meal plans data
      expect(MealPlansContainerComponent).toHaveBeenCalledWith({ mealPlans });
      expect(mockBody.appendChild).toHaveBeenCalled();
    });
  });

  describe('MealPlansContainer integration', () => {
    it('should delegate rendering to MealPlansContainer component', async () => {
      const { MealPlansContainerComponent } = await import('../components/meal-plans-container.component');
      
      const mockBody = {
        appendChild: vi.fn()
      };
      mockDocument.body = mockBody as any;
      mockDocument.getElementById.mockReturnValue(null);

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

      // PopupService should focus on data orchestration, delegate rendering to component
      expect(MealPlansContainerComponent).toHaveBeenCalledWith({ mealPlans });
      expect(mockBody.appendChild).toHaveBeenCalled();
    });
  });
});
