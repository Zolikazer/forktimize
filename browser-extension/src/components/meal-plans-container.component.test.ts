// MealPlansContainer component tests
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { MealPlansContainerComponent } from './meal-plans-container.component';
import type { MealPlansStorage } from '../services/storage-service';

// Mock DayCard component
vi.mock('./day-card.component', () => ({
  DayCardComponent: vi.fn().mockImplementation(({ date }) => ({
    render: vi.fn().mockReturnValue(() => {
      const card = document.createElement('div');
      card.className = 'day-plan';
      card.setAttribute('data-date', date);
      return card;
    })()
  }))
}));

describe('MealPlansContainerComponent', () => {
  let component: MealPlansContainerComponent;
  let mockMealPlans: MealPlansStorage;

  beforeEach(() => {
    vi.clearAllMocks();
    
    mockMealPlans = {
      '2025-01-15': {
        date: '2025-01-15',
        foodVendor: 'CityFood',
        foods: ['Chicken Rice'],
        exportedAt: '2025-01-15T10:00:00Z',
        addedAt: '2025-01-15T10:00:00Z'
      },
      '2025-01-14': {
        date: '2025-01-14',
        foodVendor: 'InterFood',
        foods: ['Beef Stew'],
        exportedAt: '2025-01-14T10:00:00Z',
        addedAt: '2025-01-14T10:00:00Z'
      },
      '2025-01-16': {
        date: '2025-01-16',
        foodVendor: 'eFood',
        foods: ['Pizza'],
        exportedAt: '2025-01-16T10:00:00Z',
        addedAt: '2025-01-16T10:00:00Z'
      }
    };

    component = new MealPlansContainerComponent({ mealPlans: mockMealPlans });
  });

  describe('render', () => {
    it('should create a container with correct structure', () => {
      const container = component.render();

      expect(container.tagName).toBe('DIV');
      expect(container.id).toBe('meal-plans-container');
    });

    it('should create DayCard components for each meal plan', async () => {
      const { DayCardComponent } = await import('./day-card.component');
      
      const container = component.render();

      // Should create 3 DayCard components
      expect(DayCardComponent).toHaveBeenCalledTimes(3);
      
      // Should create cards for each date with correct plans
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: '2025-01-14',
        plan: mockMealPlans['2025-01-14']
      });
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: '2025-01-15',
        plan: mockMealPlans['2025-01-15']
      });
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: '2025-01-16',
        plan: mockMealPlans['2025-01-16']
      });
    });

    it('should sort meal plans chronologically', () => {
      const container = component.render();
      const cards = Array.from(container.children);

      expect(cards).toHaveLength(3);
      
      // Should be sorted: 01-14, 01-15, 01-16
      expect(cards[0].getAttribute('data-date')).toBe('2025-01-14');
      expect(cards[1].getAttribute('data-date')).toBe('2025-01-15');
      expect(cards[2].getAttribute('data-date')).toBe('2025-01-16');
    });

    it('should handle empty meal plans', () => {
      const emptyComponent = new MealPlansContainerComponent({ mealPlans: {} });
      const container = emptyComponent.render();

      expect(container.tagName).toBe('DIV');
      expect(container.id).toBe('meal-plans-container');
      expect(container.children).toHaveLength(0);
      expect(container.innerHTML).toBe('');
    });

    it('should handle single meal plan', () => {
      const singlePlan = {
        '2025-01-15': mockMealPlans['2025-01-15']
      };
      const singleComponent = new MealPlansContainerComponent({ mealPlans: singlePlan });
      const container = singleComponent.render();

      expect(container.children).toHaveLength(1);
      expect(container.children[0].getAttribute('data-date')).toBe('2025-01-15');
    });

    it('should sort dates correctly across different months', () => {
      const crossMonthPlans = {
        '2025-02-01': {
          date: '2025-02-01',
          foodVendor: 'CityFood',
          foods: ['February Food'],
          exportedAt: '2025-02-01T10:00:00Z',
          addedAt: '2025-02-01T10:00:00Z'
        },
        '2025-01-31': {
          date: '2025-01-31',
          foodVendor: 'InterFood',
          foods: ['January Food'],
          exportedAt: '2025-01-31T10:00:00Z',
          addedAt: '2025-01-31T10:00:00Z'
        },
        '2025-01-15': {
          date: '2025-01-15',
          foodVendor: 'eFood',
          foods: ['Mid January Food'],
          exportedAt: '2025-01-15T10:00:00Z',
          addedAt: '2025-01-15T10:00:00Z'
        }
      };

      const crossMonthComponent = new MealPlansContainerComponent({ mealPlans: crossMonthPlans });
      const container = crossMonthComponent.render();
      const cards = Array.from(container.children);

      // Should be sorted: 01-15, 01-31, 02-01
      expect(cards[0].getAttribute('data-date')).toBe('2025-01-15');
      expect(cards[1].getAttribute('data-date')).toBe('2025-01-31');
      expect(cards[2].getAttribute('data-date')).toBe('2025-02-01');
    });

    it('should handle dates in random order and sort them correctly', () => {
      const randomOrderPlans = {
        '2025-01-20': mockMealPlans['2025-01-15'], // Reusing plan data
        '2025-01-10': mockMealPlans['2025-01-14'],
        '2025-01-25': mockMealPlans['2025-01-16'],
        '2025-01-05': mockMealPlans['2025-01-15']
      };

      const randomComponent = new MealPlansContainerComponent({ mealPlans: randomOrderPlans });
      const container = randomComponent.render();
      const cards = Array.from(container.children);

      // Should be sorted chronologically
      expect(cards[0].getAttribute('data-date')).toBe('2025-01-05');
      expect(cards[1].getAttribute('data-date')).toBe('2025-01-10');
      expect(cards[2].getAttribute('data-date')).toBe('2025-01-20');
      expect(cards[3].getAttribute('data-date')).toBe('2025-01-25');
    });
  });

  describe('integration', () => {
    it('should render complete container with all DayCard components', () => {
      const container = component.render();
      
      // Verify overall structure
      expect(container.id).toBe('meal-plans-container');
      expect(container.children.length).toBe(3);
      
      // Verify all cards are properly mounted
      const cards = Array.from(container.children);
      cards.forEach(card => {
        expect(card.className).toBe('day-plan');
        expect(card.getAttribute('data-date')).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      });
    });

    it('should maintain component composition', async () => {
      const { DayCardComponent } = await import('./day-card.component');
      
      component.render();
      
      // Verify DayCard components were created (basic integration test)
      expect(DayCardComponent).toHaveBeenCalled();
      expect(DayCardComponent).toHaveBeenCalledWith({
        date: expect.any(String),
        plan: expect.any(Object)
      });
    });
  });
});