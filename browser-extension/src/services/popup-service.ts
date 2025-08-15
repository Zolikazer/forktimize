// PopupService - Clean TypeScript popup logic using our services
import { StorageService, type MealPlansStorage } from './services/storage-service';
import { MessageService } from './services/message-service';

interface ButtonState {
  PROCESSING: string;
  SUCCESS: string;
  FAILED: string;
  DEFAULT: string;
}

export class PopupService {
  private readonly UI_TEXT: ButtonState = {
    PROCESSING: '⏳ Adding...',
    SUCCESS: '✅ Added!',
    FAILED: '❌ Failed',
    DEFAULT: '🛒 Add to Cart'
  };

  constructor(
    private storageService: StorageService,
    private messageService: MessageService,
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
      <div class="auto-cart-section">
        <button class="auto-cart-btn" 
                data-date="${this.escapeHtml(date)}" 
                data-vendor="${this.escapeHtml(vendorName)}">
          ${this.UI_TEXT.DEFAULT}
        </button>
      </div>
    `;

    // Add click handler
    const button = card.querySelector('.auto-cart-btn') as HTMLButtonElement;
    if (button) {
      button.addEventListener('click', () => {
        this.handleAutoCartClick(button, plan);
      });
    }

    return card;
  }

  private async handleAutoCartClick(button: HTMLButtonElement, plan: any) {
    const date = button.getAttribute('data-date');
    const vendor = button.getAttribute('data-vendor');
    
    if (!date || !vendor) return;

    console.log('🛒 Auto-cart clicked for:', date, vendor);
    
    this.setButtonState(button, 'PROCESSING');
    
    try {
      const currentTab = await this.messageService.getCurrentTab();
      if (!currentTab.id) throw new Error('No active tab');

      await this.messageService.sendAutoCartMessage(currentTab.id, {
        date,
        vendor,
        foods: plan.foods || []
      });

      this.setButtonState(button, 'SUCCESS');
    } catch (error) {
      console.error('Auto-cart failed:', error);
      this.setButtonState(button, 'FAILED');
    }
  }

  private setButtonState(button: HTMLButtonElement, state: keyof ButtonState) {
    button.disabled = state === 'PROCESSING';
    button.textContent = this.UI_TEXT[state];
    
    if (state === 'SUCCESS' || state === 'FAILED') {
      setTimeout(() => {
        button.disabled = false;
        button.textContent = this.UI_TEXT.DEFAULT;
      }, 2000);
    }
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