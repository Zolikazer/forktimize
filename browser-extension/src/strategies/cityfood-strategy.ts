// CityFood-specific cart automation strategy
import { BaseVendorStrategy } from './base-vendor-strategy';
import { DomService } from '../services/dom-service';

export class CityFoodStrategy extends BaseVendorStrategy {
  constructor(private domService: DomService) {
    super();
  }

  getVendorId(): string {
    return 'cityfood';
  }

  async searchFood(foodName: string, targetDate: string): Promise<HTMLElement> {
    console.log(`🔍 CityFood: Searching for "${foodName}" for date ${targetDate}`);
    
    // Extract the existing cart service logic for finding food
    const foodData = await this.findFoodData(foodName, targetDate);
    return foodData.targetFoodElement;
  }

  validateFood(element: HTMLElement, expectedName: string, targetDate: string): boolean {
    console.log(`🔍 CityFood: Validating "${expectedName}" for date ${targetDate}`);
    
    const dayIndex = this.domService.getDateIndex(targetDate);
    if (dayIndex === -1) {
      console.error(`❌ CityFood: Date ${targetDate} not available`);
      return false;
    }

    // Use existing validation logic from cart service
    return this.domService.validateFoodMatch(element, expectedName, dayIndex, targetDate);
  }

  async addToCart(element: HTMLElement): Promise<boolean> {
    console.log('🛒 CityFood: Adding food to cart');
    
    try {
      // Use existing cart service logic
      const success = this.domService.clickAddButton(element);
      if (!success) {
        throw new Error('Failed to click add button');
      }
      console.log('✅ CityFood: Successfully added to cart');
      return true;
    } catch (error) {
      console.error('❌ CityFood: Failed to add to cart:', error);
      return false;
    }
  }

  // Private methods extracted from existing cart service logic
  private async findFoodData(foodName: string, targetDate: string) {
    const foodElement = this.findFoodElement(foodName);
    const category = this.findFoodCategory(foodElement);
    const dayIndex = this.getTargetDayIndex(targetDate);
    const targetFoodElement = this.getTargetFoodElement(category, dayIndex);
    
    this.validateFoodAtTarget(targetFoodElement, foodName, dayIndex, targetDate);
    
    return { targetFoodElement };
  }

  private findFoodElement(foodName: string): HTMLElement {
    const foodElement = this.domService.findFoodByName(foodName);
    if (!foodElement) {
      throw new Error(`Food "${foodName}" not found`);
    }
    return foodElement as HTMLElement;
  }

  private findFoodCategory(foodElement: HTMLElement): HTMLElement {
    const category = this.domService.findCategory(foodElement);
    if (!category) {
      throw new Error('Could not find category for food');
    }
    return category as HTMLElement;
  }

  private getTargetDayIndex(targetDate: string): number {
    const dayIndex = this.domService.getDateIndex(targetDate);
    if (dayIndex === -1) {
      throw new Error(`Date ${targetDate} not available`);
    }
    return dayIndex;
  }

  private getTargetFoodElement(category: HTMLElement, dayIndex: number): HTMLElement {
    const targetFoodElement = this.domService.getFoodAtPosition(category, dayIndex);
    if (!targetFoodElement) {
      throw new Error(`No food at position ${dayIndex}`);
    }
    return targetFoodElement as HTMLElement;
  }

  private validateFoodAtTarget(
    targetFoodElement: HTMLElement, 
    foodName: string, 
    dayIndex: number, 
    targetDate: string
  ): void {
    const isValid = this.domService.validateFoodMatch(
      targetFoodElement, 
      foodName, 
      dayIndex, 
      targetDate
    );
    if (!isValid) {
      throw new Error('Food name mismatch at target position');
    }
  }
}