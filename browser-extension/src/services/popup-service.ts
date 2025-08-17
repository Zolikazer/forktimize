// PopupService - Clean TypeScript popup logic using our services
import { StorageService, type MealPlansStorage } from './storage-service';
import { MealPlansContainerComponent } from '../components/meal-plans-container.component';

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
    const existingContainer = this.document.getElementById('meal-plans-container');
    if (existingContainer) {
      existingContainer.remove();
    }

    const containerComponent = new MealPlansContainerComponent({ mealPlans });
    const containerElement = containerComponent.render();
    
    // Mount to the parent element (assuming it exists)
    const parentElement = this.document.body || this.document.documentElement;
    parentElement.appendChild(containerElement);
  }
}
