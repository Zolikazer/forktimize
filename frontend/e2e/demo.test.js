import {expect, test} from '@playwright/test';

test("User can generate a menu and interact with it", async ({page}) => {
    await page.goto("/menu_creator"); // Change if needed

    await expect(page.locator("text=Set Your Nutritional Goals")).toBeVisible();
    await expect(page.locator("text=No menu generated yet")).toBeVisible();

    const dateSelect = page.locator("select");
    await dateSelect.selectOption({index: 1}); // Select second date in the dropdown

    const blacklistInput = page.locator('input[placeholder="Type a food and press Enter"]');
    await blacklistInput.fill("Broccoli");
    await blacklistInput.press("Enter");
    await blacklistInput.fill("Csoki");
    await blacklistInput.press("Enter");

    const blacklistedFood = page.locator(".tag", { hasText: "Csoki" });
    await expect(blacklistedFood).toBeVisible();

    const removeBlacklistBtn = blacklistedFood.locator("button.delete");
    await removeBlacklistBtn.click();

    await expect(blacklistedFood).not.toBeVisible();

    const generateButton = page.getByRole("button", {name: "Generate My Menu"});
    await generateButton.click();

    const menuStatus = page.getByText("Your menu is ready.");
    await expect(menuStatus).toBeVisible({timeout: 5000});

    const menuItems = page.locator(".food-card");
    await expect(menuItems.first()).toBeVisible({timeout: 5000});
    const menuItemsCount = await menuItems.count();

    await expect(menuItems.first()).toBeVisible({timeout: 5000});

    await expect(page.locator("text=Total Cost:")).toBeVisible();
    await expect(page.locator("text=Total Calories:")).toBeVisible();

    const removeButton = menuItems.first().locator("button:has-text('🤮 Nem szeretem')");
    await removeButton.click();

    await expect(await menuItems.count()).toBeLessThan(menuItemsCount);
});

