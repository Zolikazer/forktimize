// PopupService - Clean TypeScript popup logic using our services
import { StorageService, type MealPlansStorage } from './storage-service';
import { DayCardComponent } from '../components/day-card.component';

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
    const dayCard = new DayCardComponent({ date, plan });
    return dayCard.render();
  }
}
