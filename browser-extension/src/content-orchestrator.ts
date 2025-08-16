// Content script orchestration - functional approach with dependency injection
import type { CartService } from './services/cart-service';
import type { MessageService } from './services/message-service';
import type { StorageService } from './services/storage-service';

export function setupContentScript(
  cartService: CartService,
  messageService: MessageService,
  storageService: StorageService
) {
  setupExtensionHandshake(messageService);
  setupMealPlanHandler(messageService, storageService);
  setupAutoCartHandler(messageService, cartService);
}

function setupExtensionHandshake(messageService: MessageService) {
  messageService.onExtensionSyn(() => {
    console.log('🤝 Received SYN from frontend, sending ACK');
    messageService.sendExtensionAck();
    console.log('✅ Extension handshake protocol completed');
  });
}

function setupMealPlanHandler(messageService: MessageService, storageService: StorageService) {
  messageService.onMealPlanData(async (data) => {
    await handleMealPlanData(data, storageService);
  });
}

function setupAutoCartHandler(messageService: MessageService, cartService: CartService) {
  messageService.onAutoCart(async (data, sendResponse) => {
    await handleAutoCart(data, sendResponse, cartService);
  });
}

export async function handleMealPlanData(data: any, storageService: StorageService) {
  console.log('🔥 Meal plan data received:', data);
  
  try {
    await storageService.saveMealPlan(data);
    console.log(`✅ Meal plan for ${data.date} saved successfully!`);
    showSuccessAlert(`🎉 Meal plan for ${data.date} sent to extension!`);
  } catch (error) {
    console.error('❌ Failed to save meal plan:', error);
    showErrorAlert('❌ Failed to save meal plan to extension');
  }
}

export async function handleAutoCart(data: any, sendResponse: (response: any) => void, cartService: CartService) {
  console.log('🛒 Auto-cart request received:', data);
  
  try {
    const results = await cartService.processAutoCart(data);
    const successCount = results.filter(r => r.success).length;
    const totalCount = results.length;
    
    if (successCount === totalCount) {
      sendResponse({ 
        success: true, 
        message: `Successfully added all ${successCount} foods to cart!`,
        results 
      });
    } else {
      sendResponse({ 
        success: false, 
        message: `Added ${successCount}/${totalCount} foods to cart`,
        results 
      });
    }
  } catch (error) {
    console.error('❌ Auto-cart failed:', error);
    const errorMessage = extractErrorMessage(error);
    sendResponse({ 
      success: false, 
      message: `Auto-cart failed: ${errorMessage}`,
      error: errorMessage 
    });
  }
}

// Private helper functions (not exported)
function extractErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'Unknown error';
}

function showSuccessAlert(message: string) {
  alert(message);
}

function showErrorAlert(message: string) {
  alert(message);
}