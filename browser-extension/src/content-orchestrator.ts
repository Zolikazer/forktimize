// Content script orchestration - functional approach with dependency injection
import type { CartService } from './services/cart-service';
import type { StorageService } from './services/storage-service';
import { onExtensionSyn, sendExtensionAck, onMealPlanData, onAutoCart } from './lib/messaging';

export function setupContentScript(
  cartService: CartService,
  storageService: StorageService
) {
  setupExtensionHandshake();
  setupMealPlanHandler(storageService);
  setupAutoCartHandler(cartService);
}

function setupExtensionHandshake() {
  onExtensionSyn(() => {
    console.log('🤝 Received SYN from frontend, sending ACK');
    sendExtensionAck();
    console.log('✅ Extension handshake protocol completed');
  });
}

function setupMealPlanHandler(storageService: StorageService) {
  onMealPlanData(async (data) => {
    await handleMealPlanData(data, storageService);
  });
}

function setupAutoCartHandler(cartService: CartService) {
  onAutoCart(async (data, sendResponse) => {
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
