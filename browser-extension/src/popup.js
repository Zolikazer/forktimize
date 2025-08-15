// Cross-browser API
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

// Get constants
const { MESSAGE_TYPES, UI_TEXT } = window.FORKTIMIZE_CONSTANTS;

// ButtonStateManager - Centralized button state management
const ButtonStateManager = {
  setProcessing(button) {
    button.disabled = true;
    button.textContent = UI_TEXT.BUTTON_PROCESSING;
  },

  setSuccess(button, duration = 2000) {
    button.textContent = UI_TEXT.BUTTON_SUCCESS;
    this._resetAfterDelay(button, duration);
  },

  setError(button, duration = 2000) {
    button.textContent = UI_TEXT.BUTTON_FAILED;
    this._resetAfterDelay(button, duration);
  },

  reset(button) {
    button.disabled = false;
    button.textContent = UI_TEXT.BUTTON_DEFAULT;
  },

  _resetAfterDelay(button, duration) {
    setTimeout(() => {
      this.reset(button);
    }, duration);
  }
};

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

// Template Functions - Clean HTML generation
const Templates = {
  dayCard(date, plan) {
    const formattedDate = this.formatDate(date);
    const foodsListHtml = this.generateFoodsList(plan.foods);
    const vendorName = plan.foodVendor || 'Unknown Vendor';
    
    return `
      <div class="day-header">${formattedDate}</div>
      <div class="vendor-info">📍 ${this.escapeHtml(vendorName)}</div>
      <div class="foods-list">
        ${foodsListHtml}
      </div>
      <div class="auto-cart-section">
        ${this.autoCartButton(date, plan.foodVendor)}
      </div>
    `;
  },

  formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short', 
      day: 'numeric'
    });
  },

  generateFoodsList(foods) {
    if (!foods || foods.length === 0) {
      return 'No foods listed';
    }
    
    return foods
      .map(food => this.extractFoodName(food))
      .map(foodName => `• ${this.escapeHtml(foodName)}`)
      .join('<br>');
  },

  extractFoodName(food) {
    if (typeof food === 'object') {
      return food.name || 'Unnamed food';
    }
    return food;
  },

  autoCartButton(date, vendor) {
    return `
      <button class="auto-cart-btn" 
              data-date="${this.escapeHtml(date)}" 
              data-vendor="${this.escapeHtml(vendor || '')}">
        ${UI_TEXT.BUTTON_DEFAULT}
      </button>
    `;
  },

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
};

function createDayCard(date, plan) {
  const card = document.createElement('div');
  card.className = 'day-plan';
  
  card.innerHTML = Templates.dayCard(date, plan);
  
  return card;
}

function setupAutoCartHandlers(mealPlans) {
  const autoCartButtons = document.querySelectorAll('.auto-cart-btn');
  
  autoCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      handleAutoCartClick(e.target, mealPlans);
    });
  });
}

async function handleAutoCartClick(button, mealPlans) {
  const clickData = extractButtonData(button);
  const plan = mealPlans[clickData.date];
  
  console.log('🛒 Auto-cart clicked for:', clickData.date, clickData.vendor);
  
  ButtonStateManager.setProcessing(button);
  
  try {
    await sendAutoCartMessage(clickData, plan);
    ButtonStateManager.setSuccess(button);
  } catch (error) {
    console.error('Auto-cart failed:', error);
    ButtonStateManager.setError(button);
  }
}

function extractButtonData(button) {
  return {
    date: button.getAttribute('data-date'),
    vendor: button.getAttribute('data-vendor')
  };
}

async function sendAutoCartMessage(clickData, plan) {
  const [tab] = await browserAPI.tabs.query({ active: true, currentWindow: true });
  
  await browserAPI.tabs.sendMessage(tab.id, {
    type: MESSAGE_TYPES.AUTO_CART,
    data: {
      date: clickData.date,
      vendor: clickData.vendor,
      foods: plan.foods || []
    }
  });
}

// Listen for storage changes to update UI in real-time
browserAPI.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.forktimizeMealPlans) {
    loadMealPlans();
  }
});