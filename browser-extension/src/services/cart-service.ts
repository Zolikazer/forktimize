// CartService - Business logic orchestrator for auto-cart functionality
import { DomService, type DomSelectors } from './dom-service';
import { StorageService, type MealPlan } from './storage-service';

export interface CartResult {
  food: string;
  success: boolean;
  error?: string;
}

export interface AutoCartRequest {
  date: string;
  vendor: string;
  foods: Array<string | { name: string }>;
}

export interface VendorConfig {
  hostname: string;
  selectors: DomSelectors;
  name: string;
}

export class CartService {
  private readonly PROCESSING_DELAY = 500; // ms between foods

  constructor(
    private domService: DomService,
    private storageService: StorageService,
    private vendorConfig: VendorConfig
  ) {}

  // Main auto-cart flow
  async processAutoCart(request: AutoCartRequest): Promise<CartResult[]> {
    console.log('🛒 Starting auto-cart for:', request);

    // Validate we're on the correct vendor site
    if (!this.domService.validateSiteHostname(this.vendorConfig.hostname)) {
      throw new Error(`Not on ${this.vendorConfig.name} site`);
    }

    // Process each food with functional approach
    const results = await this.#processFoodsSequentially(request.foods, request.date);
    
    // Save successful cart operation to storage
    await this.#saveCartResults(request, results);

    return results;
  }

  // Individual food processing
  async addFoodToCart(foodName: string, targetDate: string): Promise<boolean> {
    console.log(`🔍 Processing food: "${foodName}" for date: ${targetDate}`);

    try {
      // Step 1: Find the food element
      const foodElement = this.domService.findFoodByName(foodName);
      if (!foodElement) {
        throw new Error(`Food "${foodName}" not found`);
      }

      // Step 2: Get the category for positional logic
      const category = this.domService.findCategory(foodElement);
      if (!category) {
        throw new Error('Could not find category for food');
      }

      // Step 3: Convert date to day index
      const dayIndex = this.domService.getDateIndex(targetDate);
      if (dayIndex === -1) {
        throw new Error(`Date ${targetDate} not available`);
      }

      // Step 4: Get food at the target position
      const targetFoodElement = this.domService.getFoodAtPosition(category, dayIndex);
      if (!targetFoodElement) {
        throw new Error(`No food at position ${dayIndex}`);
      }

      // Step 5: Validate the food matches what we expect
      const isValid = this.domService.validateFoodMatch(
        targetFoodElement, 
        foodName, 
        dayIndex, 
        targetDate
      );
      if (!isValid) {
        throw new Error('Food name mismatch at target position');
      }

      // Step 6: Click the add button
      const success = this.domService.clickAddButton(targetFoodElement);
      if (!success) {
        throw new Error('Failed to click add button');
      }

      console.log(`✅ Successfully added "${foodName}" to cart`);
      return true;

    } catch (error) {
      console.error(`❌ Failed to add "${foodName}":`, error);
      return false;
    }
  }

  // Bulk food validation
  async validateFoodsAvailable(foods: string[], targetDate: string): Promise<{
    available: string[];
    missing: string[];
    dateAvailable: boolean;
  }> {
    // Check if target date is available
    const availableDates = this.domService.getAvailableDates();
    const dateAvailable = availableDates.includes(targetDate);

    if (!dateAvailable) {
      return {
        available: [],
        missing: foods,
        dateAvailable: false
      };
    }

    // Find which foods are available
    const foodMap = this.domService.findFoodsWithNames(foods);
    const available = foods.filter(food => foodMap.get(food) !== null);
    const missing = foods.filter(food => foodMap.get(food) === null);

    return { available, missing, dateAvailable };
  }

  // Category analysis for debugging
  analyzeFoodAvailability(foods: string[]): {
    totalCategories: number;
    categoriesWithAllFoods: number;
    foodDistribution: Record<string, number>;
  } {
    const categories = Array.from(document.querySelectorAll(this.vendorConfig.selectors.CATEGORY));
    
    const analysis = categories.map(category => 
      this.domService.analyzeCategoryStructure(category)
    );

    const categoriesWithAllFoods = analysis
      .filter(cat => cat.hasAllFoods(foods))
      .length;

    // Count food distribution across categories
    const foodDistribution = foods.reduce((acc, food) => {
      acc[food] = analysis.filter(cat => cat.foodTitles.includes(food)).length;
      return acc;
    }, {} as Record<string, number>);

    return {
      totalCategories: categories.length,
      categoriesWithAllFoods,
      foodDistribution
    };
  }

  // Private helper methods
  async #processFoodsSequentially(
    foods: Array<string | { name: string }>, 
    targetDate: string
  ): Promise<CartResult[]> {
    const results: CartResult[] = [];

    for (const food of foods) {
      const foodName = this.#extractFoodName(food);
      
      const success = await this.addFoodToCart(foodName, targetDate);
      results.push({ 
        food: foodName, 
        success,
        error: success ? undefined : `Failed to add ${foodName} to cart`
      });
      
      // Add delay between foods to avoid overwhelming the site
      if (foods.indexOf(food) < foods.length - 1) {
        await this.#delay(this.PROCESSING_DELAY);
      }
    }

    return results;
  }

  #extractFoodName(food: string | { name: string }): string {
    return typeof food === 'object' ? food.name : food;
  }

  #delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async #saveCartResults(request: AutoCartRequest, results: CartResult[]): Promise<void> {
    const successfulFoods = results
      .filter(result => result.success)
      .map(result => result.food);

    if (successfulFoods.length === 0) {
      console.log('No foods added to cart, skipping storage save');
      return;
    }

    try {
      // Load existing meal plan and update with cart results
      const existingPlan = await this.storageService.loadMealPlan(request.date);
      
      const updatedPlan: Omit<MealPlan, 'addedAt'> = {
        date: request.date,
        foodVendor: request.vendor,
        foods: existingPlan?.foods || request.foods,
        exportedAt: existingPlan?.exportedAt || new Date().toISOString()
      };

      // Add metadata about cart operation
      (updatedPlan as any).cartResults = {
        addedToCart: successfulFoods,
        processedAt: new Date().toISOString(),
        totalRequested: results.length,
        totalSuccessful: successfulFoods.length
      };

      await this.storageService.saveMealPlan(updatedPlan);
      console.log(`💾 Saved cart results for ${request.date}`);
      
    } catch (error) {
      console.error('Failed to save cart results to storage:', error);
      // Don't throw - cart operation was successful even if save failed
    }
  }
}