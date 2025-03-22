import {fireEvent, render, screen, waitFor} from "@testing-library/svelte";
import {beforeEach, describe, expect, test, vi} from "vitest";
import Input from "$lib/components/input/Input.svelte";
import * as FoodPlannerClient from "$lib/api/foodPlannerClient.js";
import {menuStatus, menu, MenuGenerationStatus, menuStore} from "$lib/stores/menuStore.js";
import {get} from "svelte/store";


beforeEach(() => {
    menuStore.reset()
});


vi.mock("$lib/foodPlannerClient.js");

describe("Input Component", () => {
    test("renders all macro constraint inputs", () => {
        render(Input);

        expect(screen.getByText(/Calories/i)).toBeInTheDocument();
        expect(screen.getByText(/Protein/i)).toBeInTheDocument();
        expect(screen.getByText(/Carb/i)).toBeInTheDocument();
        expect(screen.getByText(/Fat/i)).toBeInTheDocument();
    });

    test("renders date selector and food blacklist", () => {
        render(Input);

        expect(screen.getByText(/Select a Date/i)).toBeInTheDocument();
        expect(screen.getByText(/Foods You Dislike/i)).toBeInTheDocument();

    });

    test("generates menu when clicking 'Generate My Menu'", async () => {
        const mockFoods = [{name: "Mocked Food", kcal: 500}];
        vi.spyOn(FoodPlannerClient, "getMenuPlan").mockResolvedValue({
            foods: mockFoods,
            foodLogEntry: {chicken: 500, sugar: 200, oil: 10}
        });

        render(Input);

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);

        console.log(get(menuStore))

        expect(get(menuStore).foods).toEqual(mockFoods);
    });

    test('disables button while fetching', async () => {
        const mockMenu = {foods: [], foodLogEntry: {chicken: 0, sugar: 0, oil: 0}};

        const delayedResponse = new Promise(resolve => setTimeout(() => resolve(mockMenu), 200));
        vi.spyOn(FoodPlannerClient, 'getMenuPlan').mockImplementation(() => delayedResponse);

        render(Input);
        const button = screen.getByRole('button', {name: /Generate My Menu/i});

        expect(button).not.toBeDisabled();

        fireEvent.click(button);

        await waitFor(() => {
            expect(button).toBeDisabled();
        });
    });

});
