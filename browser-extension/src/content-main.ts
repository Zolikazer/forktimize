// TypeScript content script - clean orchestrator using MessageService
import { StorageService } from './services/storage-service';
import { MessageService } from './services/message-service';

console.log('TypeScript content script loaded on:', window.location.hostname);

const storageService = new StorageService();
const messageService = new MessageService();

// Extension handshake protocol
messageService.onExtensionSyn(() => {
  console.log('🤝 Received SYN from frontend, sending ACK');
  messageService.sendExtensionAck();
  console.log('✅ Extension handshake protocol completed');
});

// Meal plan data handling
messageService.onMealPlanData(async (data) => {
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

// Auto-cart handling (placeholder for future)
messageService.onAutoCart(async (data, sendResponse) => {
  console.log('🛒 Auto-cart request received:', data);
  // TODO: Implement cart automation when we refactor that part
  sendResponse({ success: false, message: 'Auto-cart not implemented yet' });
});