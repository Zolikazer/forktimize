import {render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test} from "vitest";
import {foodLogEntryStore} from "$lib/stores/menuStore.js";
import FoodLogEntry from "$lib/components/menu/FoodLogEntry.svelte";

beforeEach(() => {
    foodLogEntryStore.set({
        chicken: 350,
        sugar: 180,
        oil: 45
    });
});
describe("FoodLogEntrySummary", () => {

    test("renders the macro values correctly", () => {
        render(FoodLogEntry);

        expect(screen.getByText(/Chicken Breast/i)).toBeInTheDocument();
        expect(screen.getByText(/350g/i)).toBeInTheDocument();

        expect(screen.getByText(/Sugar/i)).toBeInTheDocument();
        expect(screen.getByText(/180g/i)).toBeInTheDocument();

        expect(screen.getByText(/Olive Oil/i)).toBeInTheDocument();
        expect(screen.getByText(/45g/i)).toBeInTheDocument();
    });

    test("renders informative description box", () => {
        render(FoodLogEntry);

        expect(screen.getByText(/this format lets you log it quickly/i)).toBeInTheDocument();
    });
});
