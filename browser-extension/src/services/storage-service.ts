// StorageService - Clean meal plan storage abstraction
export interface MealPlan {
  date: string;
  foodVendor: string;
  foods: Array<string | { name: string }>;
  exportedAt: string;
  addedAt: string;
}

export interface MealPlansStorage {
  [date: string]: MealPlan;
}

export class StorageService {
  private readonly storageKey = 'forktimizeMealPlans';
  private readonly lastUpdatedKey = 'lastUpdated';

  constructor(
    private browserAPI = typeof (globalThis as any).browser !== 'undefined' 
      ? (globalThis as any).browser 
      : (globalThis as any).chrome
  ) {}

  async saveMealPlan(mealPlanData: Omit<MealPlan, 'addedAt'>): Promise<void> {
    const existingPlans = await this.#loadAllPlans();
    
    existingPlans[mealPlanData.date] = {
      ...mealPlanData,
      addedAt: new Date().toISOString()
    };
    
    await this.browserAPI.storage.local.set({
      [this.storageKey]: existingPlans,
      [this.lastUpdatedKey]: new Date().toISOString()
    });
  }

  async loadMealPlan(date: string): Promise<MealPlan | null> {
    const allPlans = await this.#loadAllPlans();
    return allPlans[date] || null;
  }

  async loadAllMealPlans(): Promise<MealPlansStorage> {
    return this.#loadAllPlans();
  }

  async deleteMealPlan(date: string): Promise<void> {
    const existingPlans = await this.#loadAllPlans();
    delete existingPlans[date];
    
    await this.browserAPI.storage.local.set({
      [this.storageKey]: existingPlans,
      [this.lastUpdatedKey]: new Date().toISOString()
    });
  }

  async clearAllMealPlans(): Promise<void> {
    await this.browserAPI.storage.local.set({
      [this.storageKey]: {},
      [this.lastUpdatedKey]: new Date().toISOString()
    });
  }

  onStorageChange(callback: (changes: MealPlansStorage) => void): void {
    this.browserAPI.storage.onChanged.addListener((changes: any, namespace: string) => {
      if (namespace === 'local' && changes[this.storageKey]) {
        callback(changes[this.storageKey].newValue || {});
      }
    });
  }

  // Private methods
  async #loadAllPlans(): Promise<MealPlansStorage> {
    const result = await this.browserAPI.storage.local.get([this.storageKey]);
    return result[this.storageKey] || {};
  }
}