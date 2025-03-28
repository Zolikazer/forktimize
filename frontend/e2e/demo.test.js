import {expect, test} from '@playwright/test';
import {menuCreatorPage} from "./menuCreatorPage.js";


test.describe('Menu Creator', () => {
    test.beforeEach(async ({ page }) => {
        await menuCreatorPage.goto(page);
    });

    test('initial state is correct', async ({ page }) => {
        await expect(page.getByText("Set Your Nutritional Goals")).toBeVisible();
        await expect(page.getByText("No menu generated yet")).toBeVisible();
    });

    test('user can blacklist and remove foods', async ({ page }) => {
        await menuCreatorPage.addDislikedFood(page, 'Broccoli');
        await menuCreatorPage.addDislikedFood(page, 'Csoki');

        await expect(menuCreatorPage.getBlacklistedFoodTag(page, 'Csoki')).toBeVisible();

        await menuCreatorPage.removeDislikedFood(page, 'Csoki');
        await expect(menuCreatorPage.getBlacklistedFoodTag(page, 'Csoki')).not.toBeVisible();
    });

    test('user can generate menu', async ({ page }) => {
        await menuCreatorPage.selectDate(page, 1);
        await menuCreatorPage.generateMenu(page);

        await expect(page.getByText("Your menu is ready.")).toBeVisible({ timeout: 5000 });

        const menuItems = page.locator(".food-card");
        await expect(menuItems.first()).toBeVisible({ timeout: 5000 });

        await expect(page.locator(".card-header-title", { hasText: "Your Meal Plan" })).toBeVisible();
        await expect(page.locator(".tag.is-success", { hasText: /🔥.*calories/i })).toBeVisible();
        await expect(page.locator(".tag.is-success", { hasText: /Ft/i })).toBeVisible();

        await expect(page.locator(".macro-box", { hasText: /Protein/i })).toBeVisible();
        await expect(page.locator(".macro-box", { hasText: /Carbs/i })).toBeVisible();
        await expect(page.locator(".macro-box", { hasText: /Fat/i })).toBeVisible();
    });

    test('user can remove food from generated menu', async ({ page }) => {
        await menuCreatorPage.selectDate(page, 1);
        await menuCreatorPage.generateMenu(page);

        const menuItems = page.locator(".food-card");
        await expect(menuItems.first()).toBeVisible({ timeout: 5000 });


        const initialMenuItemCount = await menuItems.count();

        await menuCreatorPage.removeFoodFromMenu(page, menuItems.first());

        await expect(await menuItems.count()).toBeLessThan(initialMenuItemCount);
    });

    test('generates different menus for different days and constraints', async ({ page }) => {
        await menuCreatorPage.goto(page);

        await menuCreatorPage.selectDate(page, 0);
        await menuCreatorPage.generateMenu(page);
        const firstMenu = await menuCreatorPage.getMenuFoodNames(page);

        await menuCreatorPage.selectDate(page, 1);
        await menuCreatorPage.setMacroConstraint(page, 'Protein', { min: 200, max: 250 });
        await menuCreatorPage.generateMenu(page);

        await expect(async () => {
            const secondMenu = await menuCreatorPage.getMenuFoodNames(page);
            expect(secondMenu).not.toEqual(firstMenu);
        }).toPass({ timeout: 5000 });
    });
});
