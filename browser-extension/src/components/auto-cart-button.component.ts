// AutoCartButton component - Handles auto-cart button UI and messaging
import { BaseComponent } from './base/base-component';
import { sendAutoCartMessage, getCurrentTab } from '../lib/messaging';
import type { MealPlan } from '../services/storage-service';

export interface AutoCartButtonProps {
  plan: MealPlan;
}

export class AutoCartButtonComponent extends BaseComponent<AutoCartButtonProps> {
  private readonly UI_TEXT = {
    PROCESSING: '⏳ Adding...',
    SUCCESS: '✅ Added!',
    FAILED: '❌ Failed',
    DEFAULT: '🛒 Add to Cart'
  };

  render(): HTMLElement {
    const button = document.createElement('button');
    button.className = 'auto-cart-btn';
    button.textContent = this.UI_TEXT.DEFAULT;
    
    button.addEventListener('click', () => {
      this.handleClick(button);
    });
    
    return button;
  }

  private async handleClick(button: HTMLButtonElement): Promise<void> {
    const { plan } = this.props;
    
    console.log('🛒 Auto-cart clicked for:', plan.date, plan.foodVendor);

    this.setButtonState(button, 'PROCESSING');

    try {
      const currentTab = await getCurrentTab();
      if (!currentTab.id) throw new Error('No active tab');

      await sendAutoCartMessage(currentTab.id, {
        date: plan.date,
        vendor: plan.foodVendor,
        foods: plan.foods
      });

      this.setButtonState(button, 'SUCCESS');
    } catch (error) {
      console.error('Auto-cart failed:', error);
      this.setButtonState(button, 'FAILED');
    }
  }

  private setButtonState(button: HTMLButtonElement, state: keyof typeof this.UI_TEXT): void {
    button.disabled = state === 'PROCESSING';
    button.textContent = this.UI_TEXT[state];

    if (state === 'SUCCESS' || state === 'FAILED') {
      setTimeout(() => {
        button.disabled = false;
        button.textContent = this.UI_TEXT.DEFAULT;
      }, 2000);
    }
  }
}