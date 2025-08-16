import { describe, it, expect, vi, beforeEach } from 'vitest';
import { setupContentScript, handleMealPlanData, handleAutoCart } from './content-orchestrator';
import type { CartService } from './services/cart-service';
import type { MessageService } from './services/message-service';
import type { StorageService } from './services/storage-service';

// Mock services
const createMockCartService = (): CartService => ({
  processAutoCart: vi.fn(),
  addFoodToCart: vi.fn(),
  validateFoodsAvailable: vi.fn(),
  analyzeFoodAvailability: vi.fn()
} as any);

const createMockMessageService = (): MessageService => ({
  onExtensionSyn: vi.fn(),
  onMealPlanData: vi.fn(),
  onAutoCart: vi.fn(),
  sendExtensionAck: vi.fn(),
  sendAutoCartMessage: vi.fn(),
  getCurrentTab: vi.fn()
} as any);

const createMockStorageService = (): StorageService => ({
  saveMealPlan: vi.fn(),
  loadMealPlan: vi.fn(),
  loadAllMealPlans: vi.fn(),
  clearMealPlan: vi.fn(),
  clearAllMealPlans: vi.fn()
} as any);

describe('Content Orchestrator', () => {
  let mockCartService: CartService;
  let mockMessageService: MessageService;
  let mockStorageService: StorageService;

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Mock global alert
    global.alert = vi.fn();
    
    mockCartService = createMockCartService();
    mockMessageService = createMockMessageService();
    mockStorageService = createMockStorageService();
  });

  describe('setupContentScript', () => {
    it('should setup all message handlers', () => {
      setupContentScript(mockCartService, mockMessageService, mockStorageService);

      expect(mockMessageService.onExtensionSyn).toHaveBeenCalledWith(expect.any(Function));
      expect(mockMessageService.onMealPlanData).toHaveBeenCalledWith(expect.any(Function));
      expect(mockMessageService.onAutoCart).toHaveBeenCalledWith(expect.any(Function));
    });

    it('should setup extension handshake correctly', () => {
      setupContentScript(mockCartService, mockMessageService, mockStorageService);

      // Get the callback that was passed to onExtensionSyn
      const handshakeCallback = (mockMessageService.onExtensionSyn as any).mock.calls[0][0];
      
      // Execute the callback
      handshakeCallback();

      expect(mockMessageService.sendExtensionAck).toHaveBeenCalled();
    });
  });

  describe('handleMealPlanData', () => {
    const testMealPlanData = {
      date: '2025-01-15',
      foodVendor: 'cityfood',
      foods: ['Pizza', 'Salad'],
      exportedAt: '2025-01-15T10:00:00Z'
    };

    it('should save meal plan data successfully', async () => {
      (mockStorageService.saveMealPlan as any).mockResolvedValue(undefined);

      await handleMealPlanData(testMealPlanData, mockStorageService);

      expect(mockStorageService.saveMealPlan).toHaveBeenCalledWith(testMealPlanData);
      expect(global.alert).toHaveBeenCalledWith('🎉 Meal plan for 2025-01-15 sent to extension!');
    });

    it('should handle save errors gracefully', async () => {
      const saveError = new Error('Storage failed');
      (mockStorageService.saveMealPlan as any).mockRejectedValue(saveError);

      await handleMealPlanData(testMealPlanData, mockStorageService);

      expect(mockStorageService.saveMealPlan).toHaveBeenCalledWith(testMealPlanData);
      expect(global.alert).toHaveBeenCalledWith('❌ Failed to save meal plan to extension');
    });
  });

  describe('handleAutoCart', () => {
    const testAutoCartData = {
      date: '2025-01-15',
      vendor: 'cityfood',
      foods: ['Pizza', 'Salad']
    };

    it('should process auto-cart successfully when all foods added', async () => {
      const mockResults = [
        { food: 'Pizza', success: true },
        { food: 'Salad', success: true }
      ];
      (mockCartService.processAutoCart as any).mockResolvedValue(mockResults);
      const mockSendResponse = vi.fn();

      await handleAutoCart(testAutoCartData, mockSendResponse, mockCartService);

      expect(mockCartService.processAutoCart).toHaveBeenCalledWith(testAutoCartData);
      expect(mockSendResponse).toHaveBeenCalledWith({
        success: true,
        message: 'Successfully added all 2 foods to cart!',
        results: mockResults
      });
    });

    it('should handle partial failures', async () => {
      const mockResults = [
        { food: 'Pizza', success: true },
        { food: 'Salad', success: false, error: 'Not found' }
      ];
      (mockCartService.processAutoCart as any).mockResolvedValue(mockResults);
      const mockSendResponse = vi.fn();

      await handleAutoCart(testAutoCartData, mockSendResponse, mockCartService);

      expect(mockCartService.processAutoCart).toHaveBeenCalledWith(testAutoCartData);
      expect(mockSendResponse).toHaveBeenCalledWith({
        success: false,
        message: 'Added 1/2 foods to cart',
        results: mockResults
      });
    });

    it('should handle cart service errors', async () => {
      const cartError = new Error('Cart service failed');
      (mockCartService.processAutoCart as any).mockRejectedValue(cartError);
      const mockSendResponse = vi.fn();

      await handleAutoCart(testAutoCartData, mockSendResponse, mockCartService);

      expect(mockCartService.processAutoCart).toHaveBeenCalledWith(testAutoCartData);
      expect(mockSendResponse).toHaveBeenCalledWith({
        success: false,
        message: 'Auto-cart failed: Cart service failed',
        error: 'Cart service failed'
      });
    });

    it('should handle unknown errors', async () => {
      const unknownError = 'Something weird happened';
      (mockCartService.processAutoCart as any).mockRejectedValue(unknownError);
      const mockSendResponse = vi.fn();

      await handleAutoCart(testAutoCartData, mockSendResponse, mockCartService);

      expect(mockSendResponse).toHaveBeenCalledWith({
        success: false,
        message: 'Auto-cart failed: Unknown error',
        error: 'Unknown error'
      });
    });

    it('should call sendResponse exactly once', async () => {
      const mockResults = [{ food: 'Pizza', success: true }];
      (mockCartService.processAutoCart as any).mockResolvedValue(mockResults);
      const mockSendResponse = vi.fn();

      await handleAutoCart(testAutoCartData, mockSendResponse, mockCartService);

      expect(mockSendResponse).toHaveBeenCalledTimes(1);
    });
  });

  describe('Integration - message handler callbacks', () => {
    it('should wire meal plan handler correctly', async () => {
      setupContentScript(mockCartService, mockMessageService, mockStorageService);
      (mockStorageService.saveMealPlan as any).mockResolvedValue(undefined);

      // Get the callback that was passed to onMealPlanData
      const mealPlanCallback = (mockMessageService.onMealPlanData as any).mock.calls[0][0];
      
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      await mealPlanCallback(testData);

      expect(mockStorageService.saveMealPlan).toHaveBeenCalledWith(testData);
    });

    it('should wire auto-cart handler correctly', async () => {
      setupContentScript(mockCartService, mockMessageService, mockStorageService);
      (mockCartService.processAutoCart as any).mockResolvedValue([{ food: 'Pizza', success: true }]);

      // Get the callback that was passed to onAutoCart
      const autoCartCallback = (mockMessageService.onAutoCart as any).mock.calls[0][0];
      
      const testData = { date: '2025-01-15', foods: ['Pizza'] };
      const mockSendResponse = vi.fn();
      await autoCartCallback(testData, mockSendResponse);

      expect(mockCartService.processAutoCart).toHaveBeenCalledWith(testData);
      expect(mockSendResponse).toHaveBeenCalled();
    });
  });
});