import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DomService, type DomSelectors } from './dom-service';

// Mock DOM setup
const createMockElement = (options: {
  tagName?: string;
  textContent?: string;
  className?: string;
  attributes?: Record<string, string>;
  children?: any[];
}): any => {
  const element = {
    tagName: options.tagName || 'DIV',
    textContent: options.textContent || '',
    className: options.className || '',
    getAttribute: (name: string) => options.attributes?.[name] || null,
    querySelector: vi.fn(),
    querySelectorAll: vi.fn(),
    closest: vi.fn(),
    click: vi.fn()
  };

  // Setup querySelectorAll to return children
  element.querySelectorAll.mockReturnValue(options.children || []);
  
  return element;
};

const mockSelectors: DomSelectors = {
  FOOD_TITLE: '.food-title',
  FOOD_CONTAINER: '.food-item',
  CATEGORY: '.category',
  DATE_BUTTON: '.date-btn',
  ADD_BUTTON: '.add-btn'
};

describe('DomService', () => {
  let domService: DomService;
  let mockDocument: any;

  beforeEach(() => {
    mockDocument = {
      querySelectorAll: vi.fn()
    };

    domService = new DomService(mockSelectors, mockDocument);
  });

  describe('findFoodByName', () => {
    it('should find food by exact name match', () => {
      const mockFoodElement = createMockElement({ tagName: 'DIV' });
      const mockTitle = createMockElement({ 
        textContent: 'Pizza Margherita',
        tagName: 'H3' 
      });
      
      mockTitle.closest.mockReturnValue(mockFoodElement);
      mockDocument.querySelectorAll.mockReturnValue([mockTitle]);

      const result = domService.findFoodByName('Pizza Margherita');

      expect(result).toBe(mockFoodElement);
      expect(mockTitle.closest).toHaveBeenCalledWith('.food-item');
    });

    it('should return null when food not found', () => {
      const mockTitle = createMockElement({ textContent: 'Burger' });
      mockDocument.querySelectorAll.mockReturnValue([mockTitle]);

      const result = domService.findFoodByName('Pizza');

      expect(result).toBeNull();
    });

    it('should handle empty query results', () => {
      mockDocument.querySelectorAll.mockReturnValue([]);

      const result = domService.findFoodByName('Pizza');

      expect(result).toBeNull();
    });
  });

  describe('getFoodsInCategory', () => {
    it('should return array of food elements', () => {
      const food1 = createMockElement({ textContent: 'Pizza' });
      const food2 = createMockElement({ textContent: 'Burger' });
      const mockCategory = createMockElement({ children: [food1, food2] });

      const result = domService.getFoodsInCategory(mockCategory);

      expect(result).toEqual([food1, food2]);
      expect(mockCategory.querySelectorAll).toHaveBeenCalledWith('.food-item');
    });
  });

  describe('getFoodAtPosition', () => {
    it('should return food at specific index', () => {
      const foods = [
        createMockElement({ textContent: 'Monday Food' }),
        createMockElement({ textContent: 'Tuesday Food' }),
        createMockElement({ textContent: 'Wednesday Food' })
      ];
      const mockCategory = createMockElement({ children: foods });

      const result = domService.getFoodAtPosition(mockCategory, 1);

      expect(result).toBe(foods[1]);
    });

    it('should return null for out-of-bounds index', () => {
      const foods = [createMockElement({ textContent: 'Pizza' })];
      const mockCategory = createMockElement({ children: foods });

      const result = domService.getFoodAtPosition(mockCategory, 5);

      expect(result).toBeNull();
    });
  });

  describe('getDateIndex', () => {
    it('should find correct index for target date', () => {
      const dateButtons = [
        createMockElement({ attributes: { 'data-date': '2025-01-15' } }),
        createMockElement({ attributes: { 'data-date': '2025-01-16' } }),
        createMockElement({ attributes: { 'data-date': '2025-01-17' } })
      ];
      mockDocument.querySelectorAll.mockReturnValue(dateButtons);

      const result = domService.getDateIndex('2025-01-16');

      expect(result).toBe(1);
    });

    it('should return -1 for non-existing date', () => {
      const dateButtons = [
        createMockElement({ attributes: { 'data-date': '2025-01-15' } })
      ];
      mockDocument.querySelectorAll.mockReturnValue(dateButtons);

      const result = domService.getDateIndex('2025-01-99');

      expect(result).toBe(-1);
    });
  });

  describe('getAvailableDates', () => {
    it('should return array of available dates', () => {
      const dateButtons = [
        createMockElement({ attributes: { 'data-date': '2025-01-15' } }),
        createMockElement({ attributes: { 'data-date': '2025-01-16' } }),
        createMockElement({ attributes: { 'data-date': null } }) // Should be filtered out
      ];
      mockDocument.querySelectorAll.mockReturnValue(dateButtons);

      const result = domService.getAvailableDates();

      expect(result).toEqual(['2025-01-15', '2025-01-16']);
    });
  });

  describe('findFoodsWithNames', () => {
    it('should return map of food names to elements', () => {
      const pizza = createMockElement({ textContent: 'Pizza' });
      const burger = createMockElement({ textContent: 'Burger' });
      
      const pizzaTitle = createMockElement({ textContent: 'Pizza' });
      const burgerTitle = createMockElement({ textContent: 'Burger' });
      
      pizzaTitle.closest.mockReturnValue(pizza);
      burgerTitle.closest.mockReturnValue(burger);
      
      mockDocument.querySelectorAll.mockReturnValue([pizzaTitle, burgerTitle]);

      const result = domService.findFoodsWithNames(['Pizza', 'Salad']);

      expect(result.get('Pizza')).toBe(pizza);
      expect(result.get('Salad')).toBeNull();
    });
  });

  describe('analyzeCategoryStructure', () => {
    it('should analyze category and provide utility functions', () => {
      const foods = [
        createMockElement({ textContent: 'Pizza' }),
        createMockElement({ textContent: 'Burger' })
      ];
      
      foods.forEach(food => {
        const title = createMockElement({ textContent: food.textContent });
        food.querySelector.mockReturnValue(title);
      });
      
      const mockCategory = createMockElement({ children: foods });

      const analysis = domService.analyzeCategoryStructure(mockCategory);

      expect(analysis.foodCount).toBe(2);
      expect(analysis.foodTitles).toEqual(['Pizza', 'Burger']);
      expect(analysis.hasAllFoods(['Pizza'])).toBe(true);
      expect(analysis.hasAllFoods(['Pizza', 'Salad'])).toBe(false);
    });
  });

  describe('validateFoodMatch', () => {
    it('should return true for exact match', () => {
      const mockElement = createMockElement({});
      const mockTitle = createMockElement({ textContent: 'Pizza' });
      mockElement.querySelector.mockReturnValue(mockTitle);

      const result = domService.validateFoodMatch(mockElement, 'Pizza', 0, '2025-01-15');

      expect(result).toBe(true);
    });

    it('should return false for mismatch', () => {
      const mockElement = createMockElement({});
      const mockTitle = createMockElement({ textContent: 'Burger' });
      mockElement.querySelector.mockReturnValue(mockTitle);

      const result = domService.validateFoodMatch(mockElement, 'Pizza', 0, '2025-01-15');

      expect(result).toBe(false);
    });
  });

  describe('clickAddButton', () => {
    it('should click add button when found', () => {
      const mockAddButton = createMockElement({});
      const mockFoodElement = createMockElement({});
      mockFoodElement.querySelector.mockReturnValue(mockAddButton);

      const result = domService.clickAddButton(mockFoodElement);

      expect(result).toBe(true);
      expect(mockAddButton.click).toHaveBeenCalled();
    });

    it('should return false when add button not found', () => {
      const mockFoodElement = createMockElement({});
      mockFoodElement.querySelector.mockReturnValue(null);

      const result = domService.clickAddButton(mockFoodElement);

      expect(result).toBe(false);
    });
  });
});