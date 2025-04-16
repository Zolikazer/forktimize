import {expect, test} from '@playwright/test';
import {mealPlanGeneratorPage} from "./mealPlanGeneratorPage.js";


test.describe('Meal Plan Generator', () => {
    test.beforeEach(async ({ page }) => {
        await mealPlanGeneratorPage.goto(page);
    });

    test('initial state is correct', async ({ page }) => {
        await expect(page.getByText("Set Your Nutritional Goals")).toBeVisible();
        await expect(page.getByText("No meal plan generated yet")).toBeVisible();
    });

    test('user can blacklist and remove foods', async ({ page }) => {
        await mealPlanGeneratorPage.addDislikedFood(page, 'Broccoli');
        await mealPlanGeneratorPage.addDislikedFood(page, 'Csoki');

        await expect(mealPlanGeneratorPage.getBlacklistedFoodTag(page, 'Csoki')).toBeVisible();

        await mealPlanGeneratorPage.removeDislikedFood(page, 'Csoki');
        await expect(mealPlanGeneratorPage.getBlacklistedFoodTag(page, 'Csoki')).not.toBeVisible();
    });

    test('user can generate meal plan', async ({ page }) => {
        await mealPlanGeneratorPage.selectDate(page, 1);
        await mealPlanGeneratorPage.generateMealPlan(page);

        await expect(page.getByText("Your meal plan is ready.")).toBeVisible({ timeout: 5000 });

        const mealPlanItems = page.locator(".food-card");
        await expect(mealPlanItems.first()).toBeVisible({ timeout: 5000 });

        await expect(page.locator(".card-header-title", { hasText: "Your Meal Plan 🛵 Order these" })).toBeVisible();
        await expect(page.locator(".tag.is-success", { hasText: /calories/i })).toBeVisible();
        await expect(page.locator(".tag.is-success", { hasText: /Ft/i })).toBeVisible();

        await expect(page.locator(".macro-box", { hasText: /Protein/i })).toBeVisible();
        await expect(page.locator(".macro-box", { hasText: /Carb/i })).toBeVisible();
        await expect(page.locator(".macro-box", { hasText: /Fat/i })).toBeVisible();
    });

    test('user can remove food from generated meal plan', async ({ page }) => {
        await mealPlanGeneratorPage.selectDate(page, 1);
        await mealPlanGeneratorPage.generateMealPlan(page);

        const mealPlanItems = page.locator(".food-card");
        await expect(mealPlanItems.first()).toBeVisible({ timeout: 5000 });


        const initialMealPlanItemCount = await mealPlanItems.count();

        await mealPlanGeneratorPage.removeFoodFromMealPlan(page, mealPlanItems.first());

        await expect(async () => {
            await expect(await mealPlanItems.count()).toBeLessThan(initialMealPlanItemCount);
        }).toPass({ timeout: 5000 });
    });

    test('generates different meal plans for different days and constraints', async ({ page }) => {
        await mealPlanGeneratorPage.goto(page);

        await mealPlanGeneratorPage.selectDate(page, 0);
        await mealPlanGeneratorPage.generateMealPlan(page);
        const firstMealPlan = await mealPlanGeneratorPage.getMealPlanFoodNames(page);

        await mealPlanGeneratorPage.selectDate(page, 1);
        await mealPlanGeneratorPage.setMacroConstraint(page, 'Protein', { min: 200, max: 250 });
        await mealPlanGeneratorPage.generateMealPlan(page);

        await expect(async () => {
            const secondMealPlan = await mealPlanGeneratorPage.getMealPlanFoodNames(page);
            expect(secondMealPlan).not.toEqual(firstMealPlan);
        }).toPass({ timeout: 5000 });
    });
});
