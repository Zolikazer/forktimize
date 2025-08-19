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
    this.logClickInfo();
    this.setButtonState(button, 'PROCESSING');
    
    try {
      const response = await this.executeAutoCart();
      this.handleAutoCartResponse(response, button);
    } catch (error) {
      this.handleAutoCartError(error, button);
    }
  }

  private logClickInfo(): void {
    const { plan } = this.props;
    console.log('🛒 Auto-cart clicked for:', plan.date, plan.foodVendor);
  }

  private async executeAutoCart(): Promise<any> {
    const { plan } = this.props;
    const currentTab = await getCurrentTab();
    
    if (!currentTab.id) {
      throw new Error('No active tab');
    }

    return await sendAutoCartMessage(currentTab.id, {
      date: plan.date,
      vendor: plan.foodVendor,
      foods: plan.foods
    });
  }

  private handleAutoCartResponse(response: any, button: HTMLButtonElement): void {
    if (response && response.success) {
      this.setButtonState(button, 'SUCCESS');
    } else {
      this.setButtonState(button, 'FAILED', response?.message || 'Auto-cart failed');
    }
  }

  private handleAutoCartError(error: unknown, button: HTMLButtonElement): void {
    console.error('Auto-cart failed:', error);
    
    const errorMessage = error instanceof Error ? error.message : String(error);
    const isConnectionError = errorMessage.includes('Could not establish connection') || 
                             errorMessage.includes('Receiving end does not exist');
    
    if (isConnectionError) {
      this.setButtonState(button, 'FAILED', '🌐 Open CityFood in another tab first');
    } else {
      this.setButtonState(button, 'FAILED', 'Auto-cart failed');
    }
  }

  private setButtonState(button: HTMLButtonElement, state: keyof typeof this.UI_TEXT, customMessage?: string): void {
    button.disabled = state === 'PROCESSING';
    button.textContent = customMessage || this.UI_TEXT[state];

    if (state === 'SUCCESS' || state === 'FAILED') {
      setTimeout(() => {
        button.disabled = false;
        button.textContent = this.UI_TEXT.DEFAULT;
      }, 3000); // Longer timeout for error messages
    }
  }
}