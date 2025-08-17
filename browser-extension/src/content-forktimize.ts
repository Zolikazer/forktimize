// Content script for Forktimize domain - handles extension handshake and meal plan data
import { StorageService } from './services/storage-service';
import { onExtensionSyn, sendExtensionAck, onMealPlanData } from './lib/messaging';

// Initialize services
const storageService = new StorageService();

// Setup extension handshake
function setupExtensionHandshake() {
  onExtensionSyn(() => {
    console.log('🤝 Received SYN from frontend, sending ACK');
    sendExtensionAck();
    console.log('✅ Extension handshake protocol completed');
  });
}

// Setup meal plan data handler
function setupMealPlanHandler() {
  onMealPlanData(async (data) => {
    console.log('🔥 Meal plan data received:', data);

    try {
      await storageService.saveMealPlan(data);
      console.log(`✅ Meal plan for ${data.date} saved successfully!`);
      alert(`🎉 Meal plan for ${data.date} sent to extension!`);
    } catch (error) {
      console.error('❌ Failed to save meal plan:', error);
      alert('❌ Failed to save meal plan to extension');
    }
  });
}

// Initialize Forktimize content script
setupExtensionHandshake();
setupMealPlanHandler();

console.log('🚀 Forktimize content script initialized');