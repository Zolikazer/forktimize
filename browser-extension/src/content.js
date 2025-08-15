console.log('Forktimize extension loaded on:', window.location.hostname);

// Cross-browser API compatibility
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

// Get constants
const { MESSAGE_TYPES, VENDOR_SITES, CITYFOOD_SELECTORS } = window.FORKTIMIZE_CONSTANTS;

// Message Handlers - Clean separation of concerns
const MessageHandlers = {
  handleExtensionCheck() {
    window.postMessage({type: MESSAGE_TYPES.EXTENSION_PRESENT}, '*');
  },

  async handleMealPlanData(data) {
    console.log('🔥 Meal plan data received:', data);
    
    try {
      await StorageOperations.saveMealPlan(data);
      console.log(`✅ Meal plan for ${data.date} stored successfully!`);
      alert(`🎉 Meal plan for ${data.date} sent to extension!`);
    } catch (error) {
      console.error('❌ Failed to store meal plan data:', error);
      alert('❌ Failed to save meal plan to extension');
    }
  }
};

// Storage Operations - Centralized data persistence
const StorageOperations = {
  async saveMealPlan(mealPlanData) {
    const result = await browserAPI.storage.local.get(['forktimizeMealPlans']);
    const existingPlans = result.forktimizeMealPlans || {};
    
    existingPlans[mealPlanData.date] = {
      ...mealPlanData,
      addedAt: new Date().toISOString()
    };
    
    return browserAPI.storage.local.set({
      forktimizeMealPlans: existingPlans,
      lastUpdated: new Date().toISOString()
    });
  }
};

// Listen for messages from the webpage
window.addEventListener('message', (event) => {
  if (event.data.type === MESSAGE_TYPES.EXTENSION_CHECK) {
    MessageHandlers.handleExtensionCheck();
  }
  
  if (event.data.type === MESSAGE_TYPES.MEAL_PLAN_DATA) {
    MessageHandlers.handleMealPlanData(event.data.data);
  }
});

// Listen for messages from the extension popup
browserAPI.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('🔔 Content script received message:', message);
  
  if (message.type === MESSAGE_TYPES.AUTO_CART) {
    AutoCartOperations.handleAutoCart(message.data)
      .then(result => {
        console.log('✅ Auto-cart completed:', result);
        sendResponse({ success: true, result });
      })
      .catch(error => {
        console.error('❌ Auto-cart failed:', error);
        sendResponse({ success: false, error: error.message });
      });
    
    // Return true to indicate async response
    return true;
  }
});

// Auto-Cart Operations - CityFood integration
const AutoCartOperations = {
  async handleAutoCart(data) {
    console.log('🛒 Starting auto-cart for:', data);
    
    this._validateSite();
    
    const { date, foods } = data;
    const results = [];
    
    for (const food of foods) {
      try {
        const foodName = this._extractFoodName(food);
        console.log(`🔍 Processing food: ${foodName}`);
        
        const success = await this.addFoodToCart(foodName, date);
        results.push({ food: foodName, success });
        
        await this._delay(500);
        
      } catch (error) {
        console.error(`❌ Failed to add ${food}:`, error);
        results.push({ food, success: false, error: error.message });
      }
    }
    
    return results;
  },

  _validateSite() {
    if (window.location.hostname !== VENDOR_SITES.cityfood) {
      throw new Error('Not on CityFood site');
    }
  },

  _extractFoodName(food) {
    return typeof food === 'object' ? food.name : food;
  },

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },

  async addFoodToCart(foodName, targetDate) {
    console.log(`🔍 Looking for food: "${foodName}" for date: ${targetDate}`);
    
    const foodElement = FoodMatcher.findFoodByName(foodName);
    if (!foodElement) {
      console.error('❌ Food not found:', foodName);
      return false;
    }

    const category = FoodMatcher.findCategory(foodElement);
    if (!category) {
      console.error('❌ Could not find category for food');
      return false;
    }

    const dayIndex = DateUtils.getDateToDayIndex(targetDate);
    if (dayIndex === -1) {
      return false;
    }

    const targetFoodElement = FoodMatcher.getFoodAtPosition(category, dayIndex);
    if (!targetFoodElement) {
      return false;
    }

    const isValid = FoodMatcher.validateFoodMatch(targetFoodElement, foodName, dayIndex, targetDate);
    if (!isValid) {
      return false;
    }

    return CartActions.clickAddButton(targetFoodElement);
  }
};

// Food Matching Utilities - Clean DOM operations
const FoodMatcher = {
  findFoodByName(foodName) {
    const allFoodTitles = document.querySelectorAll(CITYFOOD_SELECTORS.FOOD_TITLE);
    
    for (const title of allFoodTitles) {
      if (title.textContent.trim() === foodName) {
        const foundElement = title.closest(CITYFOOD_SELECTORS.FOOD_CONTAINER);
        console.log('✅ Found food element:', foundElement);
        return foundElement;
      }
    }
    return null;
  },

  findCategory(foodElement) {
    const category = foodElement.closest(CITYFOOD_SELECTORS.CATEGORY);
    if (category) {
      console.log('📂 Found category:', category);
    }
    return category;
  },

  getFoodAtPosition(category, dayIndex) {
    const foodsInCategory = category.querySelectorAll(CITYFOOD_SELECTORS.FOOD_CONTAINER);
    console.log(`📊 Found ${foodsInCategory.length} foods in this category`);
    
    if (dayIndex >= foodsInCategory.length) {
      console.error(`❌ Day index ${dayIndex} exceeds available foods (${foodsInCategory.length})`);
      return null;
    }
    
    const targetElement = foodsInCategory[dayIndex];
    console.log('🎯 Target food element:', targetElement);
    return targetElement;
  },

  validateFoodMatch(targetFoodElement, expectedFoodName, dayIndex, targetDate) {
    const actualFoodTitle = targetFoodElement.querySelector(CITYFOOD_SELECTORS.FOOD_TITLE)?.textContent.trim();
    console.log(`🔍 Checking food at position ${dayIndex}: "${actualFoodTitle}"`);
    
    if (actualFoodTitle !== expectedFoodName) {
      console.error(`❌ Food mismatch!`);
      console.error(`   Expected: "${expectedFoodName}"`);
      console.error(`   Found:    "${actualFoodTitle}"`);
      console.error(`   Position: ${dayIndex} (date: ${targetDate})`);
      return false;
    }
    
    console.log('✅ Food name matches! Proceeding to add to cart.');
    return true;
  }
};

// Date Utilities - Date to day index conversion
const DateUtils = {
  getDateToDayIndex(targetDate) {
    const dateButtons = document.querySelectorAll(CITYFOOD_SELECTORS.DATE_BUTTON);
    
    for (let i = 0; i < dateButtons.length; i++) {
      const buttonDate = dateButtons[i].getAttribute('data-date');
      if (buttonDate === targetDate) {
        console.log(`📅 Found date ${targetDate} at index ${i}`);
        return i;
      }
    }
    
    console.error(`❌ Date ${targetDate} not found in available dates`);
    return -1;
  }
};

// Cart Actions - DOM interactions for adding to cart
const CartActions = {
  clickAddButton(foodElement) {
    const addButton = foodElement.querySelector(CITYFOOD_SELECTORS.ADD_BUTTON);
    if (!addButton) {
      console.error('❌ Could not find add button');
      return false;
    }
    
    console.log('🔘 Found add button:', addButton);
    addButton.click();
    console.log('🎉 Successfully added to cart!');
    
    return true;
  }
};