// DomService - Functional DOM utilities for food vendor sites
export interface DomSelectors {
  FOOD_TITLE: string;
  FOOD_CONTAINER: string;
  CATEGORY: string;
  DATE_BUTTON: string;
  ADD_BUTTON: string;
}

export class DomService {
  constructor(
    private selectors: DomSelectors,
    private document: Document = window.document
  ) {}

  // Food finding utilities
  findFoodByName(foodName: string): Element | null {
    const foundElement = Array.from(this.document.querySelectorAll(this.selectors.FOOD_TITLE))
      .find(title => title.textContent?.trim() === foodName)
      ?.closest(this.selectors.FOOD_CONTAINER) || null;

    if (foundElement) {
      console.log('✅ Found food element:', foundElement);
    }
    return foundElement;
  }

  findCategory(foodElement: Element): Element | null {
    const category = foodElement.closest(this.selectors.CATEGORY);
    if (category) {
      console.log('📂 Found category:', category);
    }
    return category;
  }

  getFoodsInCategory(category: Element): Element[] {
    const foods = Array.from(category.querySelectorAll(this.selectors.FOOD_CONTAINER));
    console.log(`📊 Found ${foods.length} foods in this category`);
    return foods;
  }

  getFoodAtPosition(category: Element, dayIndex: number): Element | null {
    const foodsInCategory = this.getFoodsInCategory(category);
    
    if (dayIndex >= foodsInCategory.length) {
      console.error(`❌ Day index ${dayIndex} exceeds available foods (${foodsInCategory.length})`);
      return null;
    }
    
    const targetElement = foodsInCategory[dayIndex];
    console.log('🎯 Target food element:', targetElement);
    return targetElement;
  }

  // Text extraction utilities
  getFoodTitle(foodElement: Element): string {
    return foodElement.querySelector(this.selectors.FOOD_TITLE)?.textContent?.trim() || '';
  }

  getAllFoodTitles(category: Element): string[] {
    return this.getFoodsInCategory(category)
      .map(food => this.getFoodTitle(food))
      .filter(title => title.length > 0);
  }

  validateFoodMatch(targetElement: Element, expectedName: string, dayIndex: number, targetDate: string): boolean {
    const actualName = this.getFoodTitle(targetElement);
    console.log(`🔍 Checking food at position ${dayIndex}: "${actualName}"`);
    
    const isMatch = actualName === expectedName;
    
    if (!isMatch) {
      console.error(`❌ Food mismatch!`);
      console.error(`   Expected: "${expectedName}"`);
      console.error(`   Found:    "${actualName}"`);
      console.error(`   Position: ${dayIndex} (date: ${targetDate})`);
      return false;
    }
    
    console.log('✅ Food name matches! Proceeding to add to cart.');
    return true;
  }

  // Date utilities
  findDateButtons(): Element[] {
    return Array.from(this.document.querySelectorAll(this.selectors.DATE_BUTTON));
  }

  getDateIndex(targetDate: string): number {
    const index = this.findDateButtons()
      .findIndex(button => button.getAttribute('data-date') === targetDate);
    
    if (index !== -1) {
      console.log(`📅 Found date ${targetDate} at index ${index}`);
    } else {
      console.error(`❌ Date ${targetDate} not found in available dates`);
    }
    
    return index;
  }

  getAvailableDates(): string[] {
    return this.findDateButtons()
      .map(button => button.getAttribute('data-date'))
      .filter((date): date is string => date !== null);
  }

  // Cart interaction utilities
  findAddButton(foodElement: Element): Element | null {
    const addButton = foodElement.querySelector(this.selectors.ADD_BUTTON);
    if (addButton) {
      console.log('🔘 Found add button:', addButton);
    }
    return addButton;
  }

  clickAddButton(foodElement: Element): boolean {
    const addButton = this.findAddButton(foodElement);
    if (!addButton) {
      console.error('❌ Could not find add button');
      return false;
    }
    
    (addButton as HTMLElement).click();
    console.log('🎉 Successfully clicked add button!');
    return true;
  }

  // Validation utilities
  validateSiteHostname(expectedHostname: string): boolean {
    const currentHostname = window.location.hostname;
    const isValid = currentHostname === expectedHostname;
    
    if (!isValid) {
      console.error(`❌ Expected hostname ${expectedHostname}, got ${currentHostname}`);
    }
    
    return isValid;
  }

  // Functional food searching
  findFoodsWithNames(foodNames: string[]): Map<string, Element | null> {
    const allTitles = Array.from(this.document.querySelectorAll(this.selectors.FOOD_TITLE));
    
    return new Map(
      foodNames.map(name => [
        name,
        allTitles
          .find(title => title.textContent?.trim() === name)
          ?.closest(this.selectors.FOOD_CONTAINER) || null
      ])
    );
  }

  // Category analysis utilities
  analyzeCategoryStructure(category: Element): {
    foodCount: number;
    foodTitles: string[];
    hasAllFoods: (names: string[]) => boolean;
  } {
    const foodTitles = this.getAllFoodTitles(category);
    
    return {
      foodCount: foodTitles.length,
      foodTitles,
      hasAllFoods: (names: string[]) => 
        names.every(name => foodTitles.includes(name))
    };
  }

  // Debug utilities
  logElementInfo(element: Element | null, label: string): void {
    if (element) {
      console.log(`${label}:`, {
        tagName: element.tagName,
        className: element.className,
        textContent: element.textContent?.trim().substring(0, 50)
      });
    } else {
      console.log(`${label}: null`);
    }
  }
}