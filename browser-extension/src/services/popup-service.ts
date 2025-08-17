// PopupService - Clean TypeScript popup logic using our services
import { StorageService, type MealPlansStorage } from './storage-service';
import { AutoCartButtonComponent } from '../components/auto-cart-button.component';

export class PopupService {

  constructor(
    private storageService: StorageService,
    private document: Document = window.document
  ) {}

  async initialize() {
    await this.loadAndDisplayMealPlans();
    this.storageService.onStorageChange(() => {
      this.loadAndDisplayMealPlans();
    });
  }

  private async loadAndDisplayMealPlans() {
    try {
      const mealPlans = await this.storageService.loadAllMealPlans();
      this.displayMealPlans(mealPlans);
    } catch (error) {
      console.error('Failed to load meal plans:', error);
    }
  }

  private displayMealPlans(mealPlans: MealPlansStorage) {
    const container = this.document.getElementById('meal-plans-container');
    if (!container) return;

    const planDates = Object.keys(mealPlans);
    if (planDates.length === 0) {
      return; // Keep empty state
    }

    // Sort dates and create cards
    planDates.sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
    container.innerHTML = '';

    planDates.forEach(date => {
      const plan = mealPlans[date];
      const dayCard = this.createDayCard(date, plan);
      container.appendChild(dayCard);
    });
  }

  private createDayCard(date: string, plan: any) {
    const card = this.document.createElement('div');
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


  // Utility methods
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
    const div = this.document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}
