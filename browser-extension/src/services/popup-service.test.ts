import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PopupService } from './popup-service';

// Mock DayCard component  
vi.mock('../components/day-card.component', () => ({
  DayCardComponent: vi.fn().mockImplementation(() => ({
    render: vi.fn().mockReturnValue(() => {
      const card = document.createElement('div');
      card.className = 'day-plan';
      return card;
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
    it('should handle empty meal plans', async () => {
      const mockContainer = { innerHTML: '' };
      mockDocument.getElementById.mockReturnValue(mockContainer);
      mockStorageService.loadAllMealPlans.mockResolvedValue({});

      await popupService.initialize();

      expect(mockDocument.getElementById).toHaveBeenCalledWith('meal-plans-container');
    });

    it('should create cards for meal plans using DayCard component', async () => {
      const { DayCardComponent } = await import('../components/day-card.component');
      
      const mockContainer = {
        innerHTML: '',
        appendChild: vi.fn()
      };

      mockDocument.getElementById.mockReturnValue(mockContainer);

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

      // Should create DayCard component
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: '2025-01-15',
        plan: mealPlans['2025-01-15']
      });
      
      // Should call appendChild to add the card to container
      expect(mockContainer.appendChild).toHaveBeenCalled();
    });
  });

  describe('DayCard integration', () => {
    it('should use DayCard component for card rendering', async () => {
      const { DayCardComponent } = await import('../components/day-card.component');
      
      const mockContainer = {
        appendChild: vi.fn(),
        innerHTML: ''
      };

      mockDocument.getElementById.mockReturnValue(mockContainer);

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

      // Should delegate card creation to DayCard component
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: '2025-01-15',
        plan: mealPlans['2025-01-15']
      });
      
      // PopupService should focus on orchestration, not card details
      expect(mockContainer.appendChild).toHaveBeenCalled();
    });
  });
});
