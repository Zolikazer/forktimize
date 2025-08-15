// Cross-browser API
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

document.addEventListener('DOMContentLoaded', () => {
  loadMealPlans();
});

function loadMealPlans() {
  browserAPI.storage.local.get(['forktimizeMealPlans']).then((result) => {
    const mealPlans = result.forktimizeMealPlans || {};
    displayMealPlans(mealPlans);
  }).catch((error) => {
    console.error('Failed to load meal plans:', error);
  });
}

function displayMealPlans(mealPlans) {
  const container = document.getElementById('meal-plans-container');
  
  // Check if we have any meal plans
  const planDates = Object.keys(mealPlans);
  if (planDates.length === 0) {
    return; // Keep the empty state
  }
  
  // Sort dates chronologically
  planDates.sort((a, b) => new Date(a) - new Date(b));
  
  // Clear container and build meal plan cards
  container.innerHTML = '';
  
  planDates.forEach(date => {
    const plan = mealPlans[date];
    const dayCard = createDayCard(date, plan);
    container.appendChild(dayCard);
  });
}

function createDayCard(date, plan) {
  const card = document.createElement('div');
  card.className = 'day-plan';
  
  // Format date nicely
  const formatDate = new Date(date).toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short', 
    day: 'numeric'
  });
  
  // Handle foods array - extract name from food objects
  const foodsList = plan.foods ? plan.foods.map(food => {
    // Food might be an object with a 'name' property, or just a string
    return typeof food === 'object' ? food.name || 'Unnamed food' : food;
  }).map(foodName => `• ${foodName}`).join('<br>') : 'No foods listed';
  
  card.innerHTML = `
    <div class="day-header">${formatDate}</div>
    <div class="vendor-info">📍 ${plan.foodVendor || 'Unknown Vendor'}</div>
    <div class="foods-list">
      ${foodsList}
    </div>
  `;
  
  return card;
}

// Listen for storage changes to update UI in real-time
browserAPI.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.forktimizeMealPlans) {
    loadMealPlans();
  }
});