// Popup utilities - Functional popup orchestration
import { StorageService, type MealPlansStorage } from './storage-service';
import { MealPlansContainerComponent } from '../components/meal-plans-container.component';

// Main popup initialization function
export async function initializePopup(
  storageService: StorageService,
  document: Document = window.document
): Promise<void> {
  await loadAndDisplayMealPlans(storageService, document);
  
  // Auto-refresh on storage changes
  storageService.onStorageChange(() => {
    loadAndDisplayMealPlans(storageService, document);
  });
}

// Load and display meal plans
export async function loadAndDisplayMealPlans(
  storageService: StorageService,
  document: Document
): Promise<void> {
  try {
    const mealPlans = await storageService.loadAllMealPlans();
    displayMealPlans(mealPlans, document);
  } catch (error) {
    console.error('Failed to load meal plans:', error);
  }
}

// Display meal plans using container component
export function displayMealPlans(
  mealPlans: MealPlansStorage,
  document: Document
): void {
  const existingContainer = document.getElementById('meal-plans-container');
  if (existingContainer) {
    existingContainer.remove();
  }

  const containerComponent = new MealPlansContainerComponent({ mealPlans });
  const containerElement = containerComponent.render();
  
  // Mount to the parent element
  const parentElement = document.body || document.documentElement;
  parentElement.appendChild(containerElement);
}
