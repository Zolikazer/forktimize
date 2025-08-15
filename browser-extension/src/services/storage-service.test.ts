import { describe, it, expect, beforeEach, vi } from 'vitest';
import { StorageService, type MealPlan } from './storage-service';

// Mock browser API
const mockStorageAPI = {
  storage: {
    local: {
      get: vi.fn(),
      set: vi.fn(),
    },
    onChanged: {
      addListener: vi.fn()
    }
  }
};

describe('StorageService', () => {
  let storageService: StorageService;
  let mockGet: any;
  let mockSet: any;

  beforeEach(() => {
    vi.clearAllMocks();
    mockGet = mockStorageAPI.storage.local.get;
    mockSet = mockStorageAPI.storage.local.set;
    
    // Default empty storage
    mockGet.mockResolvedValue({});
    mockSet.mockResolvedValue(undefined);
    
    storageService = new StorageService(mockStorageAPI as any);
  });

  describe('saveMealPlan', () => {
    it('should save a new meal plan with addedAt timestamp', async () => {
      const mealPlan: Omit<MealPlan, 'addedAt'> = {
        date: '2025-01-15',
        foodVendor: 'CityFood',
        foods: ['Pizza', 'Salad'],
        exportedAt: '2025-01-15T10:00:00Z'
      };

      await storageService.saveMealPlan(mealPlan);

      expect(mockGet).toHaveBeenCalledWith(['forktimizeMealPlans']);
      expect(mockSet).toHaveBeenCalledWith({
        forktimizeMealPlans: {
          '2025-01-15': expect.objectContaining({
            ...mealPlan,
            addedAt: expect.any(String)
          })
        },
        lastUpdated: expect.any(String)
      });
    });

    it('should update existing meal plan while preserving others', async () => {
      const existingPlans = {
        '2025-01-14': {
          date: '2025-01-14',
          foodVendor: 'InterFood',
          foods: ['Burger'],
          exportedAt: '2025-01-14T10:00:00Z',
          addedAt: '2025-01-14T10:30:00Z'
        }
      };
      mockGet.mockResolvedValue({ forktimizeMealPlans: existingPlans });

      const newMealPlan: Omit<MealPlan, 'addedAt'> = {
        date: '2025-01-15',
        foodVendor: 'CityFood',
        foods: ['Pizza'],
        exportedAt: '2025-01-15T10:00:00Z'
      };

      await storageService.saveMealPlan(newMealPlan);

      expect(mockSet).toHaveBeenCalledWith({
        forktimizeMealPlans: {
          ...existingPlans,
          '2025-01-15': expect.objectContaining(newMealPlan)
        },
        lastUpdated: expect.any(String)
      });
    });
  });

  describe('loadMealPlan', () => {
    it('should return meal plan for existing date', async () => {
      const existingPlan: MealPlan = {
        date: '2025-01-15',
        foodVendor: 'CityFood',
        foods: ['Pizza'],
        exportedAt: '2025-01-15T10:00:00Z',
        addedAt: '2025-01-15T10:30:00Z'
      };
      mockGet.mockResolvedValue({ 
        forktimizeMealPlans: { '2025-01-15': existingPlan } 
      });

      const result = await storageService.loadMealPlan('2025-01-15');

      expect(result).toEqual(existingPlan);
      expect(mockGet).toHaveBeenCalledWith(['forktimizeMealPlans']);
    });

    it('should return null for non-existing date', async () => {
      mockGet.mockResolvedValue({ forktimizeMealPlans: {} });

      const result = await storageService.loadMealPlan('2025-01-99');

      expect(result).toBeNull();
    });
  });

  describe('loadAllMealPlans', () => {
    it('should return all meal plans', async () => {
      const allPlans = {
        '2025-01-15': { date: '2025-01-15', foods: ['Pizza'] },
        '2025-01-16': { date: '2025-01-16', foods: ['Burger'] }
      };
      mockGet.mockResolvedValue({ forktimizeMealPlans: allPlans });

      const result = await storageService.loadAllMealPlans();

      expect(result).toEqual(allPlans);
    });

    it('should return empty object when no plans exist', async () => {
      mockGet.mockResolvedValue({});

      const result = await storageService.loadAllMealPlans();

      expect(result).toEqual({});
    });
  });

  describe('deleteMealPlan', () => {
    it('should remove specific meal plan while preserving others', async () => {
      const existingPlans = {
        '2025-01-15': { date: '2025-01-15', foods: ['Pizza'] },
        '2025-01-16': { date: '2025-01-16', foods: ['Burger'] }
      };
      mockGet.mockResolvedValue({ forktimizeMealPlans: existingPlans });

      await storageService.deleteMealPlan('2025-01-15');

      expect(mockSet).toHaveBeenCalledWith({
        forktimizeMealPlans: {
          '2025-01-16': { date: '2025-01-16', foods: ['Burger'] }
        },
        lastUpdated: expect.any(String)
      });
    });
  });

  describe('clearAllMealPlans', () => {
    it('should remove all meal plans', async () => {
      await storageService.clearAllMealPlans();

      expect(mockSet).toHaveBeenCalledWith({
        forktimizeMealPlans: {},
        lastUpdated: expect.any(String)
      });
    });
  });

  describe('onStorageChange', () => {
    it('should register storage change listener', () => {
      const callback = vi.fn();
      
      storageService.onStorageChange(callback);

      expect(mockStorageAPI.storage.onChanged.addListener).toHaveBeenCalledWith(
        expect.any(Function)
      );
    });

    it('should call callback when meal plans change', () => {
      const callback = vi.fn();
      let registeredListener: any;
      
      mockStorageAPI.storage.onChanged.addListener.mockImplementation((listener) => {
        registeredListener = listener;
      });

      storageService.onStorageChange(callback);

      // Simulate storage change
      const changes = {
        forktimizeMealPlans: {
          newValue: { '2025-01-15': { foods: ['Pizza'] } }
        }
      };
      registeredListener(changes, 'local');

      expect(callback).toHaveBeenCalledWith({ '2025-01-15': { foods: ['Pizza'] } });
    });
  });
});