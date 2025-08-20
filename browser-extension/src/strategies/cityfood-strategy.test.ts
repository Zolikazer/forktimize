import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { CityFoodStrategy } from './cityfood-strategy';
import { DomService } from '../services/dom-service';

// Mock DomService
const mockDomService = {
  findFoodByName: vi.fn(),
  findCategory: vi.fn(),
  getDateIndex: vi.fn(),
  getFoodAtPosition: vi.fn(),
  validateFoodMatch: vi.fn(),
  clickAddButton: vi.fn()
};

describe('CityFoodStrategy', () => {
  let strategy: CityFoodStrategy;
  let mockFoodElement: HTMLElement;
  let mockCategoryElement: HTMLElement;
  let mockTargetElement: HTMLElement;

  beforeEach(() => {
    strategy = new CityFoodStrategy(mockDomService as any);
    
    // Create mock DOM elements
    mockFoodElement = document.createElement('div');
    mockFoodElement.className = 'food';
    
    mockCategoryElement = document.createElement('div');
    mockCategoryElement.className = 'category';
    
    mockTargetElement = document.createElement('div');
    mockTargetElement.className = 'target-food';
    
    // Reset all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getVendorId', () => {
    it('should return cityfood vendor id', () => {
      expect(strategy.getVendorId()).toBe('cityfood');
    });
  });

  describe('searchFood', () => {
    const foodName = 'Pizza';
    const targetDate = '2025-01-15';

    beforeEach(() => {
      // Setup happy path mocks
      mockDomService.findFoodByName.mockReturnValue(mockFoodElement);
      mockDomService.findCategory.mockReturnValue(mockCategoryElement);
      mockDomService.getDateIndex.mockReturnValue(2);
      mockDomService.getFoodAtPosition.mockReturnValue(mockTargetElement);
      mockDomService.validateFoodMatch.mockReturnValue(true);
    });

    it('should successfully find and return target food element', async () => {
      const result = await strategy.searchFood(foodName, targetDate);
      
      expect(result).toBe(mockTargetElement);
      expect(mockDomService.findFoodByName).toHaveBeenCalledWith(foodName);
      expect(mockDomService.findCategory).toHaveBeenCalledWith(mockFoodElement);
      expect(mockDomService.getDateIndex).toHaveBeenCalledWith(targetDate);
      expect(mockDomService.getFoodAtPosition).toHaveBeenCalledWith(mockCategoryElement, 2);
      expect(mockDomService.validateFoodMatch).toHaveBeenCalledWith(mockTargetElement, foodName, 2, targetDate);
    });

    it('should throw error when food not found', async () => {
      mockDomService.findFoodByName.mockReturnValue(null);

      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('Food "Pizza" not found');
    });

    it('should throw error when category not found', async () => {
      mockDomService.findCategory.mockReturnValue(null);

      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('Could not find category for food');
    });

    it('should throw error when date not available', async () => {
      mockDomService.getDateIndex.mockReturnValue(-1);

      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('Date 2025-01-15 not available');
    });

    it('should throw error when no food at position', async () => {
      mockDomService.getFoodAtPosition.mockReturnValue(null);

      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('No food at position 2');
    });

    it('should throw error when food validation fails', async () => {
      mockDomService.validateFoodMatch.mockReturnValue(false);

      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('Food name mismatch at target position');
    });
  });

  describe('validateFood', () => {
    const expectedName = 'Pizza';
    const targetDate = '2025-01-15';

    it('should return true when validation passes', () => {
      mockDomService.getDateIndex.mockReturnValue(2);
      mockDomService.validateFoodMatch.mockReturnValue(true);

      const result = strategy.validateFood(mockTargetElement, expectedName, targetDate);
      
      expect(result).toBe(true);
      expect(mockDomService.getDateIndex).toHaveBeenCalledWith(targetDate);
      expect(mockDomService.validateFoodMatch).toHaveBeenCalledWith(mockTargetElement, expectedName, 2, targetDate);
    });

    it('should return false when date not available', () => {
      mockDomService.getDateIndex.mockReturnValue(-1);

      const result = strategy.validateFood(mockTargetElement, expectedName, targetDate);
      
      expect(result).toBe(false);
      expect(mockDomService.validateFoodMatch).not.toHaveBeenCalled();
    });

    it('should return false when dom validation fails', () => {
      mockDomService.getDateIndex.mockReturnValue(2);
      mockDomService.validateFoodMatch.mockReturnValue(false);

      const result = strategy.validateFood(mockTargetElement, expectedName, targetDate);
      
      expect(result).toBe(false);
    });
  });

  describe('addToCart', () => {
    it('should successfully add food to cart', async () => {
      mockDomService.clickAddButton.mockReturnValue(true);

      const result = await strategy.addToCart(mockTargetElement);
      
      expect(result).toBe(true);
      expect(mockDomService.clickAddButton).toHaveBeenCalledWith(mockTargetElement);
    });

    it('should return false when click fails', async () => {
      mockDomService.clickAddButton.mockReturnValue(false);

      const result = await strategy.addToCart(mockTargetElement);
      
      expect(result).toBe(false);
    });

    it('should handle click button errors gracefully', async () => {
      mockDomService.clickAddButton.mockImplementation(() => {
        throw new Error('Click failed');
      });

      const result = await strategy.addToCart(mockTargetElement);
      
      expect(result).toBe(false);
    });
  });

  describe('integration flow', () => {
    it('should handle complete food processing flow', async () => {
      const foodName = 'Chicken Curry';
      const targetDate = '2025-01-16';

      // Setup mocks for successful flow
      mockDomService.findFoodByName.mockReturnValue(mockFoodElement);
      mockDomService.findCategory.mockReturnValue(mockCategoryElement);
      mockDomService.getDateIndex.mockReturnValue(1);
      mockDomService.getFoodAtPosition.mockReturnValue(mockTargetElement);
      mockDomService.validateFoodMatch.mockReturnValue(true);
      mockDomService.clickAddButton.mockReturnValue(true);

      // Execute full flow
      const foundElement = await strategy.searchFood(foodName, targetDate);
      const isValid = strategy.validateFood(foundElement, foodName, targetDate);
      const addedToCart = await strategy.addToCart(foundElement);

      // Verify results
      expect(foundElement).toBe(mockTargetElement);
      expect(isValid).toBe(true);
      expect(addedToCart).toBe(true);

      // Verify all dom service calls were made
      expect(mockDomService.findFoodByName).toHaveBeenCalledWith(foodName);
      expect(mockDomService.clickAddButton).toHaveBeenCalledWith(mockTargetElement);
    });

    it('should handle flow with search failure', async () => {
      const foodName = 'Nonexistent Food';
      const targetDate = '2025-01-16';

      // Setup mocks - search fails
      mockDomService.findFoodByName.mockReturnValue(null);

      // Search should throw error
      await expect(strategy.searchFood(foodName, targetDate))
        .rejects.toThrow('Food "Nonexistent Food" not found');

      // Verify dom service was called but subsequent methods were not
      expect(mockDomService.findFoodByName).toHaveBeenCalledWith(foodName);
      expect(mockDomService.clickAddButton).not.toHaveBeenCalled();
    });

    it('should handle separate validation after successful search', async () => {
      const foodName = 'Pizza';
      const targetDate = '2025-01-16';

      // Setup mocks for successful search
      mockDomService.findFoodByName.mockReturnValue(mockFoodElement);
      mockDomService.findCategory.mockReturnValue(mockCategoryElement);
      mockDomService.getDateIndex.mockReturnValue(1);
      mockDomService.getFoodAtPosition.mockReturnValue(mockTargetElement);
      mockDomService.validateFoodMatch.mockReturnValue(true); // Search validation passes

      // Execute search
      const foundElement = await strategy.searchFood(foodName, targetDate);
      expect(foundElement).toBe(mockTargetElement);

      // Now test separate validation call with different parameters that fails
      mockDomService.validateFoodMatch.mockReturnValue(false); // Separate validation fails
      const isValid = strategy.validateFood(foundElement, 'Different Food', targetDate);

      expect(isValid).toBe(false);
    });
  });
});