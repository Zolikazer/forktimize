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