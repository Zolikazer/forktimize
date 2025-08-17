// DayCard component - Individual meal plan day display with integrated button
import { BaseComponent } from './base/base-component';
import { AutoCartButtonComponent } from './auto-cart-button.component';
import type { MealPlan } from '../services/storage-service';

export interface DayCardProps {
  date: string;
  plan: MealPlan;
}

export class DayCardComponent extends BaseComponent<DayCardProps> {
  render(): HTMLElement {
    const { date, plan } = this.props;
    
    const card = document.createElement('div');
    card.className = 'day-plan';

    const formattedDate = this.formatDate(date);
    const foodsList = this.generateFoodsList(plan.foods);
    const vendorName = plan.foodVendor || 'Unknown Vendor';

    card.innerHTML = `
      <div class="day-header">${formattedDate}</div>
      <div class="vendor-info">📍 ${this.escapeHtml(vendorName)}</div>
      <div class="foods-list">${foodsList}</div>
      <div class="auto-cart-section"></div>
    `;

    // Create and mount AutoCartButton component
    const autoCartButton = new AutoCartButtonComponent({ plan });
    const autoCartSection = card.querySelector('.auto-cart-section') as HTMLElement;
    const buttonElement = autoCartButton.render();
    autoCartSection.appendChild(buttonElement);

    return card;
  }

  // Utility methods (will move to utils later)
  private formatDate(date: string): string {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  }

  private generateFoodsList(foods: any[]): string {
    if (!foods || foods.length === 0) {
      return 'No foods listed';
    }

    return foods
      .map(food => typeof food === 'object' ? food.name : food)
      .map(foodName => `• ${this.escapeHtml(foodName || 'Unnamed food')}`)
      .join('<br>');
  }

  private escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}