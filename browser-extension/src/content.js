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
    
    // Store the meal plan data in extension storage
    browserAPI.storage.local.set({
      forktimizeMealPlan: event.data.data,
      lastUpdated: new Date().toISOString()
    }).then(() => {
      console.log('✅ Meal plan data stored successfully!');
      alert('🎉 Meal plan sent to extension successfully!');
    }).catch((error) => {
      console.error('❌ Failed to store meal plan data:', error);
      alert('❌ Failed to save meal plan to extension');
    });
  }
});