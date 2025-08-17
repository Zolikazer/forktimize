// DayCard component tests
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { DayCardComponent } from './day-card.component';
import type { MealPlan } from '../services/storage-service';

// Mock AutoCartButton component
vi.mock('./auto-cart-button.component', () => ({
  AutoCartButtonComponent: vi.fn().mockImplementation(() => ({
    render: vi.fn().mockReturnValue(document.createElement('button'))
  }))
}));

describe('DayCardComponent', () => {
  let component: DayCardComponent;
  let mockPlan: MealPlan;

  beforeEach(() => {
    mockPlan = {
      date: '2025-01-15',
      foodVendor: 'CityFood',
      foods: ['Chicken Rice', 'Beef Stew'],
      exportedAt: '2025-01-15T10:00:00Z',
      addedAt: '2025-01-15T10:00:00Z'
    };

    component = new DayCardComponent({
      date: '2025-01-15',
      plan: mockPlan
    });
  });

  describe('render', () => {
    it('should create a day card with correct structure and content', () => {
      const card = component.render();

      expect(card.tagName).toBe('DIV');
      expect(card.className).toBe('day-plan');
      
      // Check header
      const header = card.querySelector('.day-header');
      expect(header?.textContent).toBe('Wed, Jan 15');
      
      // Check vendor info
      const vendorInfo = card.querySelector('.vendor-info');
      expect(vendorInfo?.textContent).toBe('📍 CityFood');
      
      // Check foods list
      const foodsList = card.querySelector('.foods-list');
      expect(foodsList?.innerHTML).toBe('• Chicken Rice<br>• Beef Stew');
      
      // Check auto-cart section exists
      const autoCartSection = card.querySelector('.auto-cart-section');
      expect(autoCartSection).toBeTruthy();
    });

    it('should handle unknown vendor gracefully', () => {
      const planWithoutVendor = { ...mockPlan, foodVendor: undefined };
      const componentWithoutVendor = new DayCardComponent({
        date: '2025-01-15',
        plan: planWithoutVendor as any
      });

      const card = componentWithoutVendor.render();
      const vendorInfo = card.querySelector('.vendor-info');
      expect(vendorInfo?.textContent).toBe('📍 Unknown Vendor');
    });

    it('should create and mount AutoCartButton component', async () => {
      const { AutoCartButtonComponent } = await import('./auto-cart-button.component');
      
      const card = component.render();
      
      expect(AutoCartButtonComponent).toHaveBeenCalledWith({ plan: mockPlan });
      
      const componentInstance = (AutoCartButtonComponent as any).mock.results[0].value;
      expect(componentInstance.render).toHaveBeenCalled();
    });
  });

  describe('formatDate', () => {
    it('should format date correctly', () => {
      const formattedDate = (component as any).formatDate('2025-01-15');
      expect(formattedDate).toBe('Wed, Jan 15');
    });

    it('should handle different date formats', () => {
      const formattedDate = (component as any).formatDate('2025-12-25');
      expect(formattedDate).toBe('Thu, Dec 25');
    });
  });

  describe('generateFoodsList', () => {
    it('should generate foods list with string foods', () => {
      const foods = ['Pizza', 'Pasta', 'Salad'];
      const foodsList = (component as any).generateFoodsList(foods);
      expect(foodsList).toBe('• Pizza<br>• Pasta<br>• Salad');
    });

    it('should generate foods list with object foods', () => {
      const foods = [
        { name: 'Chicken Rice' },
        { name: 'Beef Stew' }
      ];
      const foodsList = (component as any).generateFoodsList(foods);
      expect(foodsList).toBe('• Chicken Rice<br>• Beef Stew');
    });

    it('should handle mixed string and object foods', () => {
      const foods = [
        'Pizza',
        { name: 'Pasta' },
        'Salad'
      ];
      const foodsList = (component as any).generateFoodsList(foods);
      expect(foodsList).toBe('• Pizza<br>• Pasta<br>• Salad');
    });

    it('should handle empty foods array', () => {
      const foodsList = (component as any).generateFoodsList([]);
      expect(foodsList).toBe('No foods listed');
    });

    it('should handle null/undefined foods', () => {
      expect((component as any).generateFoodsList(null)).toBe('No foods listed');
      expect((component as any).generateFoodsList(undefined)).toBe('No foods listed');
    });

    it('should handle foods with missing names', () => {
      const foods = [
        { name: 'Valid Food' },
        { name: null },
        { name: undefined },
        { name: '' }
      ];
      const foodsList = (component as any).generateFoodsList(foods);
      expect(foodsList).toBe('• Valid Food<br>• Unnamed food<br>• Unnamed food<br>• Unnamed food');
    });
  });

  describe('escapeHtml', () => {
    it('should escape HTML characters', () => {
      const escaped = (component as any).escapeHtml('<script>alert("xss")</script>');
      expect(escaped).toBe('&lt;script&gt;alert("xss")&lt;/script&gt;');
    });

    it('should escape quotes and ampersands', () => {
      const escaped = (component as any).escapeHtml('Chicken & "Rice" \'Special\'');
      expect(escaped).toBe('Chicken &amp; "Rice" \'Special\'');
    });

    it('should handle empty strings', () => {
      const escaped = (component as any).escapeHtml('');
      expect(escaped).toBe('');
    });
  });

  describe('integration', () => {
    it('should render complete card with all components', () => {
      const card = component.render();
      
      // Verify overall structure
      expect(card.children.length).toBe(4); // header, vendor, foods, auto-cart-section
      
      // Verify content is properly escaped and formatted
      const vendorInfo = card.querySelector('.vendor-info');
      expect(vendorInfo?.innerHTML).toBe('📍 CityFood');
      
      // Verify foods are properly formatted
      const foodsList = card.querySelector('.foods-list');
      expect(foodsList?.innerHTML).toBe('• Chicken Rice<br>• Beef Stew');
    });
  });
});