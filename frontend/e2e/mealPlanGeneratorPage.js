import {expect} from '@playwright/test';

export const mealPlanGeneratorPage = {
    goto: async (page) => await page.goto('/meal-plan-generator'),

    addDislikedFood: async (page, food) => {
        const input = page.locator('input[placeholder="Type a food and press Enter"]');
        await input.fill(food);
        await input.press('Enter');
    },

    getBlacklistedFoodTag: (page, food) => page.locator('.tag', { hasText: food }),

    removeDislikedFood: async (page, food) => {
        const tag = page.locator('.tag', { hasText: food });
        const deleteButton = tag.locator('button.delete');
        await deleteButton.click();
    },

    selectDate: async (page, index) => {
        const dateSelect = page.getByLabel(/date/i);
        await dateSelect.selectOption({ index });
    },

    generateMealPlan: async (page) => {
        const generateButton = page.getByRole('button', { name: 'Generate Meal Plan' });
        await generateButton.click();
        await expect(page.locator('.food-card').first()).toBeVisible({ timeout: 5000 });
    },

    removeFoodFromMealPlan: async (page, foodCardLocator) => {
        const removeButton = foodCardLocator.locator("button:has-text('Don\\'t Like')");
        await removeButton.click();
    },
    getMealPlanFoodNames: async (page) => {
        return await page.locator('.food-card .food-name').allTextContents();
    },
    setMacroConstraint: async (page, label, { min, max }) => {
        const constraintSection = page.locator('.input-group', { hasText: label });
        const minInput = constraintSection.locator('label:has-text("Min") ~ div input');
        const maxInput = constraintSection.locator('label:has-text("Max") ~ div input');
        if (min !== undefined) await minInput.fill(String(min));
        if (max !== undefined) await maxInput.fill(String(max));
    },
};
