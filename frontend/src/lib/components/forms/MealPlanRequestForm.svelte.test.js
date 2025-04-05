import {fireEvent, render, screen, waitFor} from "@testing-library/svelte";
import {beforeEach, describe, expect, test, vi} from "vitest";
import MealPlanRequestForm from "$lib/components/forms/MealPlanRequestForm.svelte";
import * as FoodPlannerClient from "$lib/api/foodPlannerApi.js";
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
import {get} from "svelte/store";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";


beforeEach(() => {
    mealPlanStore.reset();
    mealPlanRequestStore.reset();
});


vi.mock("$lib/foodPlannerClient.js");

describe("MealPlanRequestForm Component", () => {
    test("renders all macro constraint inputs", () => {
        render(MealPlanRequestForm);

        expect(screen.getByText(/Calories/i)).toBeInTheDocument();
        expect(screen.getByText(/Protein/i)).toBeInTheDocument();
        expect(screen.getByText(/Carb/i)).toBeInTheDocument();
        expect(screen.getByText(/Fat/i)).toBeInTheDocument();
    });

    test("renders date selector and food blacklist", () => {
        render(MealPlanRequestForm);

        expect(screen.getByText(/Select a Date/i)).toBeInTheDocument();
        expect(screen.getByText(/Foods You Dislike/i)).toBeInTheDocument();

    });

    test("generates meal plan when clicking 'Generate Meal Plan'", async () => {
        const mockFoods = [{name: "Mocked Food", kcal: 500}];
        vi.spyOn(FoodPlannerClient, "getMealPlan").mockResolvedValue({
            foods: mockFoods,
            foodLogEntry: {chicken: 500, sugar: 200, oil: 10}
        });

        render(MealPlanRequestForm);

        const dateSelect = screen.getByLabelText(/date/i);
        await fireEvent.change(dateSelect, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate Meal Plan/i});
        await fireEvent.click(button);

        expect(get(mealPlanStore).foods).toEqual(mockFoods);
    });

    test('disables button while fetching', async () => {
        const mockMealPlan = {foods: [], foodLogEntry: {chicken: 0, sugar: 0, oil: 0}};

        const delayedResponse = new Promise(resolve => setTimeout(() => resolve(mockMealPlan), 200));
        vi.spyOn(FoodPlannerClient, 'getMealPlan').mockImplementation(() => delayedResponse);

        render(MealPlanRequestForm);
        const button = screen.getByRole('button', {name: /Generate Meal Plan/i});

        expect(button).not.toBeDisabled();

        await fireEvent.click(button);

        await waitFor(() => {
            expect(button).toBeDisabled();
        });
    });

    test('should set maxFoodRepeat to 1 when checkbox is unchecked', async () => {
        render(MealPlanRequestForm);
        const checkbox = screen.getByRole('checkbox');

        await fireEvent.click(checkbox);

        expect(get(mealPlanRequestStore).maxFoodRepeat).toBe(1);
    });

    test('should maxFoodRepeat have a value of null if checkbox is checked ', async () => {
        render(MealPlanRequestForm);

        expect(get(mealPlanRequestStore).maxFoodRepeat).toBe(null);
    });

    test("sends all params on the api", async () => {
        const mockFoods = [{name: "Mocked Food", kcal: 500}];
        const apiSpy = vi.spyOn(FoodPlannerClient, "getMealPlan").mockResolvedValue({
            foods: mockFoods,
            foodLogEntry: {chicken: 500, sugar: 200, oil: 10}
        });

        render(MealPlanRequestForm);

        const dateSelect = screen.getByLabelText(/date/i);
        await fireEvent.change(dateSelect, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate Meal Plan/i});
        await fireEvent.click(button);

        const callArgs = apiSpy.mock.calls[0][0];
        expect(apiSpy).toHaveBeenCalled();
        expect(callArgs).toHaveProperty("date");
        expect(callArgs).toHaveProperty("foodBlacklist");
        expect(callArgs).toHaveProperty("nutritionalConstraints");
        expect(callArgs).toHaveProperty("maxFoodRepeat");
        expect(callArgs).toHaveProperty("foodVendor");
    });

    test('disables the generate button when at least one macro constraint is invalid', async () => {
        mealPlanRequestStore.set({
            macroConstraints: [
                {name: 'Protein', min: 200, max: 100, unit: 'g', emoji: '🍗'},
                {name: 'Carbs', min: 100, max: 300, unit: 'g', emoji: '🍞'},
            ]
        })

        render(MealPlanRequestForm);

        const button = screen.getByRole('button', {name: /generate meal plan/i});

        expect(button).toBeDisabled();
    });

});
