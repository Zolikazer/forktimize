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
    
    const container = document.createElement('div');
    container.id = 'meal-plans-container';

    const planDates = Object.keys(mealPlans);
    
    // Add clear button if there are meal plans
    if (planDates.length > 0) {
      const clearButton = new ClearButtonComponent({ storageService });
      const clearElement = clearButton.render();
      clearElement.style.marginBottom = '10px';
      container.appendChild(clearElement);
    }
    
    // Handle empty state
    if (planDates.length === 0) {
      container.innerHTML = ''; // Keep empty state as is
      return container;
    }

    // Sort dates chronologically and create DayCard components
    planDates.sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
    
    planDates.forEach(date => {
      const plan = mealPlans[date];
      const dayCard = new DayCardComponent({ date, plan });
      const cardElement = dayCard.render();
      container.appendChild(cardElement);
    });

    return container;
  }
}