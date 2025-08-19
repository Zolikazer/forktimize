// ClearButton component - Handles clearing all meal plans
import { BaseComponent } from './base/base-component';
import { StorageService } from '../services/storage-service';

export interface ClearButtonProps {
  storageService: StorageService;
}

export class ClearButtonComponent extends BaseComponent<ClearButtonProps> {
  private readonly UI_TEXT = {
    PROCESSING: '⏳ Clearing...',
    SUCCESS: '✅ Cleared!',
    DEFAULT: '🗑️ Clear All'
  };

  render(): HTMLElement {
    const button = document.createElement('button');
    button.className = 'clear-btn';
    button.textContent = this.UI_TEXT.DEFAULT;
    
    button.addEventListener('click', () => {
      this.handleClick(button);
    });
    
    return button;
  }

  private async handleClick(button: HTMLButtonElement): Promise<void> {
    // Simple confirmation
    if (!confirm('Clear all meal plans? This cannot be undone.')) {
      return;
    }

    this.setButtonState(button, 'PROCESSING');

    try {
      await this.props.storageService.clearAllMealPlans();
      this.setButtonState(button, 'SUCCESS');
    } catch (error) {
      console.error('Failed to clear meal plans:', error);
      // Reset to default on error
      this.setButtonState(button, 'DEFAULT');
    }
  }

  private setButtonState(button: HTMLButtonElement, state: keyof typeof this.UI_TEXT): void {
    button.disabled = state === 'PROCESSING';
    button.textContent = this.UI_TEXT[state];

    if (state === 'SUCCESS') {
      setTimeout(() => {
        button.disabled = false;
        button.textContent = this.UI_TEXT.DEFAULT;
      }, 2000);
    }
  }
}