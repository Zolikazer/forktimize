import {render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test} from "vitest";
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
import FoodLogEntry from "$lib/components/food-log/FoodLogEntry.svelte";

beforeEach(() => {
    mealPlanStore.setSuccess([], {
        chicken: 350,
        sugar: 180,
        oil: 45
    });
});
describe("FoodLogEntrySummary", () => {

    test("renders the macro values correctly", () => {
        render(FoodLogEntry);

        expect(screen.getByText(/Chicken Breast/i)).toBeInTheDocument();
        expect(screen.getByText(/350/i)).toBeInTheDocument();

        expect(screen.getByText(/Sugar/i)).toBeInTheDocument();
        expect(screen.getByText(/180/i)).toBeInTheDocument();

        expect(screen.getByText(/Olive Oil/i)).toBeInTheDocument();
        expect(screen.getByText(/45/i)).toBeInTheDocument();
    });

    test("renders informative description box", () => {
        render(FoodLogEntry);

        expect(screen.getByText(/this format lets you log it quickly/i)).toBeInTheDocument();
    });
});
