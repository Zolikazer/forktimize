# Multi-Vendor Browser Extension - Architecture Design Document

## 🍽️ Partial Success Handling

**Option B: Keep Original Meal Plan Intact** ✅

### **Behavior**
- When auto-cart partially succeeds (e.g., 3/5 foods added)
- **Keep meal plan unchanged** in extension storage
- Show success/failure status for each food
- User can retry failed foods or manually add them

### **Example Flow**
1. Meal plan has: Chicken Curry, Fish Soup, Veggie Pasta, Beef Stew, Greek Salad
2. Auto-cart result: 3 foods added successfully, 2 failed
3. **Meal plan storage**: Remains exactly the same (all 5 foods)
4. **User feedback**: "3/5 foods added to cart! 2 items failed: Veggie Pasta, Beef Stew"

### **Why Option B**
- ✅ **Data safety** - original meal plan never lost
- ✅ **User trust** - no risk of losing planned meals
- ✅ **Simple state management** - storage doesn't change based on cart operations
- ✅ **Clear history** - user always sees what they originally planned
- ✅ **User control** - they decide when meal planning is complete

### **Trade-offs Accepted**
- ❌ Potential duplicates if user retries (user can manually remove from cart)
- ❌ No automatic progress tracking (user relies on feedback messages)

**Philosophy: Meal plan is source of truth, cart is temporary workspace**

---

## 🏗️ Multi-Vendor Strategy Architecture

### **Core Design Philosophy**
- **Strategy Pattern**: Different vendors use different cart automation strategies
- **Configuration-Driven**: Vendor differences handled by config, not code duplication
- **Message-Driven**: Popup sends vendor context, content script adapts accordingly
- **Scalable**: Easy to add new vendors without touching core logic

### **Architecture Overview**

```typescript
// Strategy Pattern for Vendor Differences
abstract class BaseVendorStrategy {
  abstract searchFood(foodName: string): Promise<void>;
  abstract addToCart(): Promise<boolean>;
  abstract validatePage(): boolean;
  
  // Shared utilities all vendors can use
  protected waitForElement(selector: string) { /* ... */ }
  protected clickElement(selector: string) { /* ... */ }
}

// For vendors with similar UI (CityFood, eFood)
class SimilarUIStrategy extends BaseVendorStrategy {
  constructor(private config: SimilarUIVendorConfig) { super(); }
  
  async searchFood(foodName: string) {
    // Shared logic using config.selectors
    await this.clickElement(this.config.selectors.searchBox);
    // Implementation uses config, not hardcoded values
  }
}

// For vendors with completely different UI (Wolt, FoodPanda)
class CustomVendorStrategy extends BaseVendorStrategy {
  async searchFood(foodName: string) {
    // Completely different automation logic
    await this.navigateToCategory();
    await this.filterByName(foodName);
  }
}
```

### **Vendor Configuration System**

```typescript
interface VendorConfig {
  id: string;
  name: string;
  domains: string[];
  strategy: 'similar-ui' | 'custom';
  selectors?: SimilarUISelectors; // For similar-ui strategy
  customLogic?: CustomVendorStrategy; // For custom strategy
}

const VENDOR_CONFIGS = {
  cityfood: {
    id: 'cityfood',
    name: 'CityFood',
    strategy: 'similar-ui',
    domains: ['rendel.cityfood.hu'],
    selectors: {
      searchBox: '.search-input',
      searchButton: '.search-btn',
      foodResults: '.food-item',
      addToCartButton: '.add-to-cart'
    }
  },
  efood: {
    id: 'efood', 
    name: 'eFood',
    strategy: 'similar-ui', // Same strategy as CityFood!
    domains: ['rendel.efood.hu'],
    selectors: {
      // Identical to CityFood since UI is the same
      searchBox: '.search-input',
      searchButton: '.search-btn',
      foodResults: '.food-item',
      addToCartButton: '.add-to-cart'
    }
  },
  wolt: {
    id: 'wolt',
    name: 'Wolt',
    strategy: 'custom', // Completely different approach
    domains: ['wolt.com'],
    customLogic: new WoltStrategy()
  }
}
```

### **Message-Driven Vendor Context**

```typescript
// Popup sends vendor info (no content script detection needed)
const autoCartMessage = {
  type: 'FORKTIMIZE_AUTO_CART',
  data: {
    date: '2025-01-15',
    vendor: 'efood', // 👈 Popup knows the vendor!
    foods: ['Pizza', 'Salad']
  }
};

// Content script receives vendor and adapts
onAutoCart(({ vendor, foods }, sendResponse) => {
  const vendorConfig = VENDOR_CONFIGS[vendor];
  if (!vendorConfig) {
    throw new Error(`Unsupported vendor: ${vendor}`);
  }
  
  const strategy = VendorStrategyFactory.create(vendorConfig);
  const cartService = new CartService(strategy);
  
  cartService.processAutoCart(foods);
});
```

### **Strategy Factory Pattern**

```typescript
class VendorStrategyFactory {
  static create(vendorConfig: VendorConfig): BaseVendorStrategy {
    switch (vendorConfig.strategy) {
      case 'similar-ui':
        return new SimilarUIStrategy(vendorConfig);
      case 'custom':
        return vendorConfig.customLogic;
      default:
        throw new Error(`Unsupported strategy: ${vendorConfig.strategy}`);
    }
  }
}
```

### **Clean CartService Implementation**

```typescript
class CartService {
  constructor(private strategy: BaseVendorStrategy) {}
  
  async processAutoCart(foods: string[]): Promise<CartResult> {
    // Validate we're on the right vendor page
    if (!this.strategy.validatePage()) {
      throw new Error('Wrong vendor page');
    }
    
    const results = [];
    
    // Process each food using vendor-specific strategy
    for (const food of foods) {
      try {
        await this.strategy.searchFood(food);
        await this.strategy.addToCart();
        results.push({ food, success: true });
      } catch (error) {
        results.push({ food, success: false, error: error.message });
      }
    }
    
    return { results, totalProcessed: foods.length };
  }
}
```

---

## 🚀 Implementation Plan

### **Phase 1: Foundation (No Breaking Changes)**
1. **Create strategy interfaces** (`BaseVendorStrategy`, vendor types)
2. **Extract CityFood logic** into `SimilarUIStrategy` 
3. **Create vendor config system** with CityFood config

### **Phase 2: Integration (Wire Everything Together)**
4. **Add eFood config** (same strategy, different domain)
5. **Update messaging** to pass vendor from popup
6. **Create strategy factory** pattern
7. **Refactor CartService** to use strategies

### **Phase 3: Deployment (Enable Multi-Vendor)**
8. **Update manifest files** for eFood domains
9. **Update supported vendors** list in handshake
10. **Comprehensive testing** for both vendors

### **Benefits of This Architecture**

#### **For Similar Vendors (CityFood/eFood):**
- ✅ **Maximum code reuse** - Same strategy, different config
- ✅ **Easy maintenance** - Update selectors in one place
- ✅ **Type safety** - Shared interfaces prevent errors

#### **For Different Vendors (Wolt, FoodPanda):**
- ✅ **Complete flexibility** - Custom strategy per vendor
- ✅ **No constraints** - Each can have totally different logic
- ✅ **Clean separation** - No messy vendor-specific if/else chains

#### **For the System:**
- ✅ **Popup-driven** - No complex vendor detection in content scripts
- ✅ **Scalable** - Add vendors without touching core logic
- ✅ **Testable** - Mock strategies for different test scenarios
- ✅ **Future-proof** - Architecture handles any vendor differences

---

## 🎯 Current Status

### **✅ Completed Features**
- ✅ **Vendor Support Check**: Extension validates vendor support during handshake
- ✅ **Frontend Integration**: Smart button states (enabled/disabled) based on vendor support
- ✅ **CityFood Support**: Full auto-cart functionality working
- ✅ **Cross-browser Compatibility**: Chrome and Firefox support
- ✅ **Strategy Pattern Foundation**: BaseVendorStrategy interface with shared utilities
- ✅ **CityFood Strategy**: Extracted all cart logic into testable strategy pattern
- ✅ **Comprehensive Testing**: 29/29 tests passing for strategy layer

### **🚧 Multi-Vendor Implementation Progress**

#### **Phase 1: Foundation** ✅
1. ✅ **Create strategy interfaces** (`BaseVendorStrategy`, vendor types)
2. ✅ **Extract CityFood logic** into `CityFoodStrategy` with full test coverage
3. 🚧 **Create vendor config system** with CityFood config

#### **Phase 2: Integration** 🎯
4. ⏳ **Add eFood config** (same strategy, different domain)
5. ⏳ **Update messaging** to pass vendor from popup
6. ⏳ **Create strategy factory** pattern
7. ⏳ **Refactor CartService** to use strategies

#### **Phase 3: Deployment** 🔮
8. ⏳ **Update manifest files** for eFood domains
9. ⏳ **Update supported vendors** list in handshake
10. ⏳ **Comprehensive testing** for both vendors

### **🎯 Next Steps**
1. **Vendor Configuration System** - Create config objects for CityFood/eFood
2. **Strategy Factory** - Pattern to instantiate correct strategy based on vendor
3. **CartService Integration** - Wire everything together with message-driven vendor context

**Target Vendors:**
- **CityFood** ✅ (strategy implemented & tested)
- **eFood** 🎯 (next target - identical UI to CityFood)  
- **Wolt** 🔮 (future - different UI, custom strategy)

**Current Status**: Foundation complete, ready for configuration and integration phases.

**Philosophy: Build it right once, scale effortlessly** 🔥