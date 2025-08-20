import { describe, it, expect, beforeEach, vi } from 'vitest';
import { initializePopup, loadAndDisplayMealPlans, displayMealPlans } from './popup';

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

describe('Popup Functions', () => {
  let mockDocument: any;

  beforeEach(() => {
    vi.clearAllMocks();
    mockDocument = createMockDocument();
  });

  describe('initializePopup', () => {
    it('should load meal plans and setup storage listener', async () => {
      mockStorageService.loadAllMealPlans.mockResolvedValue({});

      await initializePopup(mockStorageService as any, mockDocument as any);

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

      displayMealPlans({}, mockDocument as any, mockStorageService as any);

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

      displayMealPlans(mealPlans, mockDocument as any, mockStorageService as any);

      // Should create MealPlansContainer component with meal plans data
      expect(MealPlansContainerComponent).toHaveBeenCalledWith({ mealPlans });
      expect(mockBody.appendChild).toHaveBeenCalled();
    });
  });

  describe('loadAndDisplayMealPlans', () => {
    it('should load data and delegate rendering to displayMealPlans', async () => {
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

      await loadAndDisplayMealPlans(mockStorageService as any, mockDocument as any);

      // Should load data and delegate rendering to component
      expect(mockStorageService.loadAllMealPlans).toHaveBeenCalled();
      expect(MealPlansContainerComponent).toHaveBeenCalledWith({ mealPlans, storageService: mockStorageService });
      expect(mockBody.appendChild).toHaveBeenCalled();
    });
  });
});
