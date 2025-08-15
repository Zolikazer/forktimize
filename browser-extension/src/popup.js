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
  
  // Add click handlers for auto-cart buttons
  setupAutoCartHandlers(mealPlans);
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
    <div class="auto-cart-section">
      <button class="auto-cart-btn" data-date="${date}" data-vendor="${plan.foodVendor}">
        🛒 Auto-Add to Cart
      </button>
    </div>
  `;
  
  return card;
}

function setupAutoCartHandlers(mealPlans) {
  const autoCartButtons = document.querySelectorAll('.auto-cart-btn');
  
  autoCartButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const date = e.target.getAttribute('data-date');
      const vendor = e.target.getAttribute('data-vendor');
      const plan = mealPlans[date];
      
      console.log('🛒 Auto-cart clicked for:', date, vendor);
      
      // Disable button during processing
      button.disabled = true;
      button.textContent = '🔄 Processing...';
      
      try {
        // Send message to content script
        const [tab] = await browserAPI.tabs.query({ active: true, currentWindow: true });
        
        await browserAPI.tabs.sendMessage(tab.id, {
          type: 'FORKTIMIZE_AUTO_CART',
          data: {
            date: date,
            vendor: vendor,
            foods: plan.foods || []
          }
        });
        
        // Success feedback
        button.textContent = '✅ Added to Cart!';
        setTimeout(() => {
          button.disabled = false;
          button.textContent = '🛒 Auto-Add to Cart';
        }, 2000);
        
      } catch (error) {
        console.error('Auto-cart failed:', error);
        button.textContent = '❌ Failed';
        setTimeout(() => {
          button.disabled = false;
          button.textContent = '🛒 Auto-Add to Cart';
        }, 2000);
      }
    });
  });
}

// Listen for storage changes to update UI in real-time
browserAPI.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.forktimizeMealPlans) {
    loadMealPlans();
  }
});