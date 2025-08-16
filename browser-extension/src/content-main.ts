// TypeScript content script - handles frontend messages
import { StorageService } from './services/storage-service';

console.log('TypeScript content script loaded on:', window.location.hostname);

const storageService = new StorageService();

// Listen for messages from the frontend
window.addEventListener('message', async (event) => {
  console.log('🔔 Content script received message:', event.data);

  // Check if extension is present
  if (event.data.type === 'FORKTIMIZE_EXTENSION_CHECK') {
    window.postMessage({ type: 'FORKTIMIZE_EXTENSION_PRESENT' }, '*');
    console.log('✅ Extension presence confirmed');
  }

  // Handle meal plan data from frontend
  if (event.data.type === 'FORKTIMIZE_MEAL_PLAN_DATA') {
    console.log('🔥 Meal plan data received:', event.data.data);
    
    try {
      await storageService.saveMealPlan(event.data.data);
      console.log(`✅ Meal plan for ${event.data.data.date} saved successfully!`);
      alert(`🎉 Meal plan for ${event.data.data.date} sent to extension!`);
    } catch (error) {
      console.error('❌ Failed to save meal plan:', error);
      alert('❌ Failed to save meal plan to extension');
    }
  }
});