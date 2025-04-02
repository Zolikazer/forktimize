import {render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test} from "vitest";
import MealPlan from "$lib/components/meal-plan/MealPlan.svelte";
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";

beforeEach(() => {
    mealPlanStore.setSuccess([
        {
            name: "Test Food 1",
            calories: 300,
            protein: 20,
            carb: 40,
            fat: 10,
            price: 1500
        },
        {
            name: "Test Food 2",
            calories: 400,
            protein: 25,
            carb: 50,
            fat: 15,
            price: 2000
        }
    ], {});
});

describe("Menu Component", () => {
    test("renders title correctly", () => {
        render(MealPlan);
        expect(screen.getByText(/Your Food Plan/i)).toBeInTheDocument();
    });

    test("renders a FoodCard component for each item in the menu", () => {
        const {container} = render(MealPlan);
        const foodComponents = container.querySelectorAll('.food-card');
        expect(foodComponents.length).toBe(2);
    });
});
