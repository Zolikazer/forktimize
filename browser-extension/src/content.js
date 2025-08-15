console.log('Forktimize extension loaded on:', window.location.hostname);

// Cross-browser API compatibility
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

// Listen for messages from the webpage
window.addEventListener('message', (event) => {
  // Check if extension is present
  if (event.data.type === 'FORKTIMIZE_EXTENSION_CHECK') {
    window.postMessage({type: 'FORKTIMIZE_EXTENSION_PRESENT'}, '*');
  }
  
  // Handle meal plan data export
  if (event.data.type === 'FORKTIMIZE_MEAL_PLAN_DATA') {
    console.log('🔥 Meal plan data received:', event.data.data);
    
    const mealPlanData = event.data.data;
    const planDate = mealPlanData.date; // Assuming the frontend sends a date field
    
    // Get existing meal plans and add/update this one
    browserAPI.storage.local.get(['forktimizeMealPlans']).then((result) => {
      const existingPlans = result.forktimizeMealPlans || {};
      
      // Add or update the meal plan for this specific date
      existingPlans[planDate] = {
        ...mealPlanData,
        addedAt: new Date().toISOString()
      };
      
      // Store updated meal plans
      return browserAPI.storage.local.set({
        forktimizeMealPlans: existingPlans,
        lastUpdated: new Date().toISOString()
      });
    }).then(() => {
      console.log(`✅ Meal plan for ${planDate} stored successfully!`);
      alert(`🎉 Meal plan for ${planDate} sent to extension!`);
    }).catch((error) => {
      console.error('❌ Failed to store meal plan data:', error);
      alert('❌ Failed to save meal plan to extension');
    });
  }
});

// Listen for messages from the extension popup
browserAPI.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('🔔 Content script received message:', message);
  
  if (message.type === 'FORKTIMIZE_AUTO_CART') {
    handleAutoCart(message.data)
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

// Auto-cart functionality for CityFood
async function handleAutoCart(data) {
  console.log('🛒 Starting auto-cart for:', data);
  
  // Check if we're on CityFood site
  if (window.location.hostname !== 'rendel.cityfood.hu') {
    throw new Error('Not on CityFood site');
  }
  
  const { date, foods } = data;
  const results = [];
  
  // Process each food
  for (const food of foods) {
    try {
      const foodName = typeof food === 'object' ? food.name : food;
      console.log(`🔍 Processing food: ${foodName}`);
      
      const success = await addFoodToCart(foodName, date);
      results.push({ food: foodName, success });
      
      // Small delay between foods
      await new Promise(resolve => setTimeout(resolve, 500));
      
    } catch (error) {
      console.error(`❌ Failed to add ${food}:`, error);
      results.push({ food, success: false, error: error.message });
    }
  }
  
  return results;
}

// The proven auto-cart function from our console testing
async function addFoodToCart(foodName, targetDate) {
  console.log(`🔍 Looking for food: "${foodName}" for date: ${targetDate}`);
  
  // Step 1: Find any food with this exact name
  const allFoodTitles = document.querySelectorAll('.food-top-title');
  let foundFoodElement = null;
  
  for (const title of allFoodTitles) {
    if (title.textContent.trim() === foodName) {
      foundFoodElement = title.closest('.food');
      console.log('✅ Found food element:', foundFoodElement);
      break;
    }
  }
  
  if (!foundFoodElement) {
    console.error('❌ Food not found:', foodName);
    return false;
  }
  
  // Step 2: Get the category this food belongs to
  const category = foundFoodElement.closest('.category');
  if (!category) {
    console.error('❌ Could not find category for food');
    return false;
  }
  
  console.log('📂 Found category:', category);
  
  // Step 3: Get all foods in this category
  const foodsInCategory = category.querySelectorAll('.food');
  console.log(`📊 Found ${foodsInCategory.length} foods in this category`);
  
  // Step 4: Convert date to day index by checking the date buttons on the page
  function getDateToDayIndex(targetDate) {
    const dateButtons = document.querySelectorAll('.date-button');
    
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
  
  const dayIndex = getDateToDayIndex(targetDate);
  if (dayIndex === -1) {
    return false;
  }
  
  // Step 5: Get the target food element
  if (dayIndex >= foodsInCategory.length) {
    console.error(`❌ Day index ${dayIndex} exceeds available foods (${foodsInCategory.length})`);
    return false;
  }
  
  const targetFoodElement = foodsInCategory[dayIndex];
  console.log('🎯 Target food element:', targetFoodElement);
  
  // Step 6: VALIDATE - Check if the food at this position actually matches our target
  const targetFoodTitle = targetFoodElement.querySelector('.food-top-title')?.textContent.trim();
  console.log(`🔍 Checking food at position ${dayIndex}: "${targetFoodTitle}"`);
  
  if (targetFoodTitle !== foodName) {
    console.error(`❌ Food mismatch!`);
    console.error(`   Expected: "${foodName}"`);
    console.error(`   Found:    "${targetFoodTitle}"`);
    console.error(`   Position: ${dayIndex} (date: ${targetDate})`);
    return false;
  }
  
  console.log('✅ Food name matches! Proceeding to add to cart.');
  
  // Step 7: Find and click the add button
  const addButton = targetFoodElement.querySelector('button[aria-label*="Kosárhoz adás:"]');
  if (!addButton) {
    console.error('❌ Could not find add button');
    return false;
  }
  
  console.log('🔘 Found add button:', addButton);
  
  // Step 8: Click the add button
  addButton.click();
  console.log('🎉 Successfully added to cart!');
  
  return true;
}