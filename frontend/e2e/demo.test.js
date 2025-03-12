import {expect, test} from '@playwright/test';

test("User can generate a menu and interact with it", async ({page}) => {
    // 1️⃣ Open the app
    await page.goto("/food"); // Change if needed

    // 2️⃣ Verify key components are visible
    await expect(page.locator("text=Set Your Nutritional Goals")).toBeVisible();
    await expect(page.locator("text=No menu generated yet")).toBeVisible();

    // 3️⃣ Select a date from DateSelector
    const dateSelect = page.locator("select");
    await dateSelect.selectOption({index: 1}); // Select second date in the dropdown

    // 5️⃣ Blacklist a food
    const blacklistInput = page.locator('input[placeholder="Type a food and press Enter"]');
    await blacklistInput.fill("Broccoli");
    await blacklistInput.press("Enter");

    // 6️⃣ Generate the menu
    const generateButton = page.getByRole("button", { name: "Generate My Menu" });
    await generateButton.click();

    // 7️⃣ Wait for the menu to be generated
    const menuItems = page.locator(".food-card");
    await expect(menuItems.first()).toBeVisible({timeout: 5000});
    const menuItemsCount = await menuItems.count();

    await expect(menuItems.first()).toBeVisible({timeout: 5000});

    // 8️⃣ Verify total calories and cost are displayed
    await expect(page.locator("text=Total Cost:")).toBeVisible();
    await expect(page.locator("text=Total Calories:")).toBeVisible();

    // 9️⃣ Remove a food item from the menu
    const removeButton = menuItems.first().locator("button:has-text('🤮 Nem szeretem')");
    await removeButton.click();

    // 1️⃣0️⃣ Verify the food item was removed
    await expect(await menuItems.count()).toBeLessThan(menuItemsCount);
});
