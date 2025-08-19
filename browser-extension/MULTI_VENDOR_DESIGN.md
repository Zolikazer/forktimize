# Multi-Vendor Browser Extension - MVP Design Document

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

## 🏪 Unsupported Vendor Handling

**Disabled Button with Tooltip Approach** ✅

### **Behavior**
- Forktimize frontend checks if current vendor is supported by extension
- **If supported** (CityFood, eFood, InterFood): Show normal "Send to Extension 📱" button
- **If unsupported** (WoltFood, etc.): Show disabled button with explanatory tooltip

### **Implementation**
```typescript
const SUPPORTED_VENDORS = ['cityfood', 'efood', 'interfood'];
const isSupported = SUPPORTED_VENDORS.includes(currentVendor);

<button 
  disabled={!isSupported}
  title={isSupported ? "Send to Extension 📱" : "Extension doesn't support this vendor yet"}
>
  Send to Extension 📱
</button>
```

### **Why This Approach**
- ✅ **User awareness** - Shows extension exists but doesn't support this vendor
- ✅ **Feature discovery** - Users learn about extension capability
- ✅ **Clear expectations** - Honest about current limitations
- ✅ **Future-friendly** - Implies support might come later

### **Visual States**
- **Supported vendor**: Normal button styling, fully functional
- **Unsupported vendor**: Grayed out button, tooltip explains limitation

**No hidden buttons, no failed attempts - just honest, discoverable UX**

## 🔄 Vendor Availability Sync Strategy

**Extension as Source of Truth** ✅

### **Two Sources of Truth Approach**
- **Backend ↔ Frontend**: Backend API provides vendor list, URLs, available dates (existing)
- **Extension ↔ Frontend**: Extension defines what vendors it supports for auto-cart

### **Why This Works**
- **Manifest constraint**: Extension must declare supported URLs in manifest anyway
- **Capability separation**: Backend knows vendor data, Extension knows automation capabilities  
- **Reduced complexity**: Only 2 sources instead of 3-way sync

### **Frontend Logic Flow**
```typescript
// 1. Check if extension exists
const extensionExists = await checkExtensionInstalled();
if (!extensionExists) {
  // Hide "Send to Extension" button completely
  return;
}

// 2. Check if extension supports current vendor
const isSupported = await browser.runtime.sendMessage({
  type: 'CHECK_VENDOR_SUPPORT', 
  vendor: currentVendor
});

// 3. Show button state accordingly
<button 
  disabled={!isSupported}
  title={isSupported ? "Send to Extension 📱" : "Extension doesn't support this vendor yet"}
>
  Send to Extension 📱
</button>
```

### **Extension Message Handler**
```typescript
// Extension responds to vendor support queries
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'CHECK_VENDOR_SUPPORT') {
    const SUPPORTED_VENDORS = ['cityfood', 'efood', 'interfood'];
    const isSupported = SUPPORTED_VENDORS.includes(message.vendor);
    sendResponse(isSupported);
  }
});
```

### **Benefits**
- ✅ **Direct capability check** - extension knows exactly what it can automate
- ✅ **No 3-way sync** - backend/frontend use existing API, extension is separate
- ✅ **Clean UX** - no button if no extension, disabled if unsupported  
- ✅ **Manifest alignment** - extension support matches declared URLs

**Philosophy: Extension owns automation capabilities, backend owns vendor data**