// MealPlansContainer component - Orchestrates multiple DayCard components
import { BaseComponent } from './base/base-component';
import { DayCardComponent } from './day-card.component';
import { ClearButtonComponent } from './clear-button.component';
import type { MealPlansStorage, StorageService } from '../services/storage-service';

export interface MealPlansContainerProps {
  mealPlans: MealPlansStorage;
  storageService: StorageService;
}

export class MealPlansContainerComponent extends BaseComponent<MealPlansContainerProps> {
  render(): HTMLElement {
    const { mealPlans, storageService } = this.props;
    const container = this.createContainer();
    const planDates = Object.keys(mealPlans);
    
    if (planDates.length === 0) {
      return this.handleEmptyState(container);
    }
    
    this.addClearButton(container, storageService);
    this.addDayCards(container, mealPlans);
    
    return container;
  }

  private createContainer(): HTMLElement {
    const container = document.createElement('div');
    container.id = 'meal-plans-container';
    return container;
  }

  private handleEmptyState(container: HTMLElement): HTMLElement {
    container.innerHTML = ''; // Keep empty state as is
    return container;
  }

  private addClearButton(container: HTMLElement, storageService: StorageService): void {
    const clearButton = new ClearButtonComponent({ storageService });
    const clearElement = clearButton.render();
    clearElement.style.marginBottom = '10px';
    container.appendChild(clearElement);
  }

  private addDayCards(container: HTMLElement, mealPlans: MealPlansStorage): void {
    const planDates = Object.keys(mealPlans);
    
    // Sort dates chronologically and create DayCard components
    planDates.sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
    
    planDates.forEach(date => {
      const plan = mealPlans[date];
      const dayCard = new DayCardComponent({ date, plan });
      const cardElement = dayCard.render();
      container.appendChild(cardElement);
    });
  }
}