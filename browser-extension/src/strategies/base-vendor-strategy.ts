// Base strategy interface for all vendors - unified contract

export abstract class BaseVendorStrategy {
  /**
   * Search for a specific food item and return the DOM element
   */
  abstract searchFood(foodName: string, targetDate: string): Promise<HTMLElement>;
  
  /**
   * Validate that the found element matches expectations
   */
  abstract validateFood(element: HTMLElement, expectedName: string, targetDate: string): boolean;
  
  /**
   * Add the specific food element to cart
   */
  abstract addToCart(element: HTMLElement): Promise<boolean>;
  
  /**
   * Get vendor-specific identifier (cityfood, efood, wolt, etc.)
   */
  abstract getVendorId(): string;
  
  // Shared utility methods all strategies can inherit
  protected async waitForElement(selector: string, timeout: number = 5000): Promise<Element> {
    return new Promise((resolve, reject) => {
      const element = document.querySelector(selector);
      if (element) {
        resolve(element);
        return;
      }
      
      const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
          observer.disconnect();
          resolve(element);
        }
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
      
      setTimeout(() => {
        observer.disconnect();
        reject(new Error(`Element ${selector} not found within ${timeout}ms`));
      }, timeout);
    });
  }
  
  protected async clickElement(selector: string): Promise<void> {
    const element = await this.waitForElement(selector);
    if (element instanceof HTMLElement) {
      element.click();
    } else {
      throw new Error(`Element ${selector} is not clickable`);
    }
  }
}