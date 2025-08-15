import { describe, it, expect, beforeEach, vi } from 'vitest';
import { CartService, type AutoCartRequest, type VendorConfig } from './cart-service';
import { DomService, type DomSelectors } from './dom-service';
import { StorageService } from './storage-service';

// Mock dependencies
const mockDomService = {
  validateSiteHostname: vi.fn(),
  findFoodByName: vi.fn(),
  findCategory: vi.fn(),
  getDateIndex: vi.fn(),
  getFoodAtPosition: vi.fn(),
  validateFoodMatch: vi.fn(),
  clickAddButton: vi.fn(),
  getAvailableDates: vi.fn(),
  findFoodsWithNames: vi.fn(),
  analyzeCategoryStructure: vi.fn()
};

const mockStorageService = {
  loadMealPlan: vi.fn(),
  saveMealPlan: vi.fn()
};

const mockVendorConfig: VendorConfig = {
  hostname: 'rendel.cityfood.hu',
  name: 'CityFood',
  selectors: {
    FOOD_TITLE: '.food-title',
    FOOD_CONTAINER: '.food-item',
    CATEGORY: '.category',
    DATE_BUTTON: '.date-btn',
    ADD_BUTTON: '.add-btn'
  }
};

describe('CartService', () => {
  let cartService: CartService;

  beforeEach(() => {
    vi.clearAllMocks();
    cartService = new CartService(
      mockDomService as any,
      mockStorageService as any,
      mockVendorConfig
    );
  });

  describe('processAutoCart', () => {
    const mockRequest: AutoCartRequest = {
      date: '2025-01-15',
      vendor: 'CityFood',
      foods: ['Pizza', 'Salad']
    };

    it('should process all foods successfully', async () => {
      // Setup mocks for successful flow
      mockDomService.validateSiteHostname.mockReturnValue(true);
      mockDomService.findFoodByName.mockReturnValue({ id: 'food1' });
      mockDomService.findCategory.mockReturnValue({ id: 'category1' });
      mockDomService.getDateIndex.mockReturnValue(0);
      mockDomService.getFoodAtPosition.mockReturnValue({ id: 'targetFood' });
      mockDomService.validateFoodMatch.mockReturnValue(true);
      mockDomService.clickAddButton.mockReturnValue(true);
      mockStorageService.loadMealPlan.mockResolvedValue(null);
      mockStorageService.saveMealPlan.mockResolvedValue(undefined);

      const results = await cartService.processAutoCart(mockRequest);

      expect(results).toHaveLength(2);
      expect(results.every(result => result.success)).toBe(true);
      expect(mockDomService.validateSiteHostname).toHaveBeenCalledWith('rendel.cityfood.hu');
      expect(mockStorageService.saveMealPlan).toHaveBeenCalled();
    });

    it('should throw error for wrong site', async () => {
      mockDomService.validateSiteHostname.mockReturnValue(false);

      await expect(cartService.processAutoCart(mockRequest))
        .rejects.toThrow('Not on CityFood site');
    });

    it('should handle partial failures gracefully', async () => {
      mockDomService.validateSiteHostname.mockReturnValue(true);
      
      // First food succeeds
      mockDomService.findFoodByName
        .mockReturnValueOnce({ id: 'food1' })
        .mockReturnValueOnce(null); // Second food fails
      
      mockDomService.findCategory.mockReturnValue({ id: 'category1' });
      mockDomService.getDateIndex.mockReturnValue(0);
      mockDomService.getFoodAtPosition.mockReturnValue({ id: 'targetFood' });
      mockDomService.validateFoodMatch.mockReturnValue(true);
      mockDomService.clickAddButton.mockReturnValue(true);
      mockStorageService.loadMealPlan.mockResolvedValue(null);
      mockStorageService.saveMealPlan.mockResolvedValue(undefined);

      const results = await cartService.processAutoCart(mockRequest);

      expect(results).toHaveLength(2);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(false);
      expect(results[1].error).toBeDefined();
      expect(results[1].error).toContain('Failed to add Salad to cart');
    });
  });

  describe('addFoodToCart', () => {
    it('should successfully add food to cart', async () => {
      const mockElement = { id: 'food' };
      const mockCategory = { id: 'category' };
      const mockTargetElement = { id: 'target' };

      mockDomService.findFoodByName.mockReturnValue(mockElement);
      mockDomService.findCategory.mockReturnValue(mockCategory);
      mockDomService.getDateIndex.mockReturnValue(1);
      mockDomService.getFoodAtPosition.mockReturnValue(mockTargetElement);
      mockDomService.validateFoodMatch.mockReturnValue(true);
      mockDomService.clickAddButton.mockReturnValue(true);

      const result = await cartService.addFoodToCart('Pizza', '2025-01-15');

      expect(result).toBe(true);
      expect(mockDomService.findFoodByName).toHaveBeenCalledWith('Pizza');
      expect(mockDomService.getDateIndex).toHaveBeenCalledWith('2025-01-15');
      expect(mockDomService.validateFoodMatch).toHaveBeenCalledWith(
        mockTargetElement, 'Pizza', 1, '2025-01-15'
      );
      expect(mockDomService.clickAddButton).toHaveBeenCalledWith(mockTargetElement);
    });

    it('should return false when food not found', async () => {
      mockDomService.findFoodByName.mockReturnValue(null);

      const result = await cartService.addFoodToCart('NonExistentFood', '2025-01-15');

      expect(result).toBe(false);
    });

    it('should return false when category not found', async () => {
      mockDomService.findFoodByName.mockReturnValue({ id: 'food' });
      mockDomService.findCategory.mockReturnValue(null);

      const result = await cartService.addFoodToCart('Pizza', '2025-01-15');

      expect(result).toBe(false);
    });

    it('should return false when date not available', async () => {
      mockDomService.findFoodByName.mockReturnValue({ id: 'food' });
      mockDomService.findCategory.mockReturnValue({ id: 'category' });
      mockDomService.getDateIndex.mockReturnValue(-1);

      const result = await cartService.addFoodToCart('Pizza', '2025-01-99');

      expect(result).toBe(false);
    });

    it('should return false when food validation fails', async () => {
      mockDomService.findFoodByName.mockReturnValue({ id: 'food' });
      mockDomService.findCategory.mockReturnValue({ id: 'category' });
      mockDomService.getDateIndex.mockReturnValue(1);
      mockDomService.getFoodAtPosition.mockReturnValue({ id: 'target' });
      mockDomService.validateFoodMatch.mockReturnValue(false);

      const result = await cartService.addFoodToCart('Pizza', '2025-01-15');

      expect(result).toBe(false);
    });

    it('should return false when click fails', async () => {
      mockDomService.findFoodByName.mockReturnValue({ id: 'food' });
      mockDomService.findCategory.mockReturnValue({ id: 'category' });
      mockDomService.getDateIndex.mockReturnValue(1);
      mockDomService.getFoodAtPosition.mockReturnValue({ id: 'target' });
      mockDomService.validateFoodMatch.mockReturnValue(true);
      mockDomService.clickAddButton.mockReturnValue(false);

      const result = await cartService.addFoodToCart('Pizza', '2025-01-15');

      expect(result).toBe(false);
    });
  });

  describe('validateFoodsAvailable', () => {
    it('should return validation results for available foods', async () => {
      mockDomService.getAvailableDates.mockReturnValue(['2025-01-15', '2025-01-16']);
      mockDomService.findFoodsWithNames.mockReturnValue(new Map([
        ['Pizza', { id: 'pizza' }],
        ['Salad', { id: 'salad' }],
        ['Burger', null]
      ]));

      const result = await cartService.validateFoodsAvailable(
        ['Pizza', 'Salad', 'Burger'], 
        '2025-01-15'
      );

      expect(result).toEqual({
        available: ['Pizza', 'Salad'],
        missing: ['Burger'],
        dateAvailable: true
      });
    });

    it('should handle unavailable date', async () => {
      mockDomService.getAvailableDates.mockReturnValue(['2025-01-15']);

      const result = await cartService.validateFoodsAvailable(
        ['Pizza'], 
        '2025-01-99'
      );

      expect(result).toEqual({
        available: [],
        missing: ['Pizza'],
        dateAvailable: false
      });
    });
  });

  describe('analyzeFoodAvailability', () => {
    it('should analyze food distribution across categories', () => {
      // Mock document.querySelectorAll
      const mockCategories = [
        { id: 'cat1' },
        { id: 'cat2' }
      ];
      
      (global as any).document = {
        querySelectorAll: vi.fn().mockReturnValue(mockCategories)
      };

      mockDomService.analyzeCategoryStructure
        .mockReturnValueOnce({
          foodTitles: ['Pizza', 'Salad'],
          hasAllFoods: (foods: string[]) => foods.every(f => ['Pizza', 'Salad'].includes(f))
        })
        .mockReturnValueOnce({
          foodTitles: ['Pizza', 'Burger'],
          hasAllFoods: (foods: string[]) => foods.every(f => ['Pizza', 'Burger'].includes(f))
        });

      const result = cartService.analyzeFoodAvailability(['Pizza', 'Salad']);

      expect(result).toEqual({
        totalCategories: 2,
        categoriesWithAllFoods: 1, // Only first category has both Pizza and Salad
        foodDistribution: {
          'Pizza': 2,  // Pizza appears in both categories
          'Salad': 1   // Salad appears in one category
        }
      });
    });
  });
});