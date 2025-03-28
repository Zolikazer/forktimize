import {fireEvent, render, screen, waitFor} from "@testing-library/svelte";
import {beforeEach, describe, expect, test, vi} from "vitest";
import MenuRequestForm from "$lib/components/forms/MenuRequestForm.svelte";
import * as FoodPlannerClient from "$lib/api/foodPlannerApi.js";
import {menuStore} from "$lib/stores/menuStore.js";
import {get} from "svelte/store";
import {menuRequestStore} from "$lib/stores/menuRequestStore.js";


beforeEach(() => {
    menuStore.reset();
    menuRequestStore.reset();
});


vi.mock("$lib/foodPlannerClient.js");

describe("MenuRequestForm Component", () => {
    test("renders all macro constraint inputs", () => {
        render(MenuRequestForm);

        expect(screen.getByText(/Calories/i)).toBeInTheDocument();
        expect(screen.getByText(/Protein/i)).toBeInTheDocument();
        expect(screen.getByText(/Carb/i)).toBeInTheDocument();
        expect(screen.getByText(/Fat/i)).toBeInTheDocument();
    });

    test("renders date selector and food blacklist", () => {
        render(MenuRequestForm);

        expect(screen.getByText(/Select a Date/i)).toBeInTheDocument();
        expect(screen.getByText(/Foods You Dislike/i)).toBeInTheDocument();

    });

    test("generates menu when clicking 'Generate My Menu'", async () => {
        const mockFoods = [{name: "Mocked Food", kcal: 500}];
        vi.spyOn(FoodPlannerClient, "getMenuPlan").mockResolvedValue({
            foods: mockFoods,
            foodLogEntry: {chicken: 500, sugar: 200, oil: 10}
        });

        render(MenuRequestForm);

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);

        expect(get(menuStore).foods).toEqual(mockFoods);
    });

    test('disables button while fetching', async () => {
        const mockMenu = {foods: [], foodLogEntry: {chicken: 0, sugar: 0, oil: 0}};

        const delayedResponse = new Promise(resolve => setTimeout(() => resolve(mockMenu), 200));
        vi.spyOn(FoodPlannerClient, 'getMenuPlan').mockImplementation(() => delayedResponse);

        render(MenuRequestForm);
        const button = screen.getByRole('button', {name: /Generate My Menu/i});

        expect(button).not.toBeDisabled();

        await fireEvent.click(button);

        await waitFor(() => {
            expect(button).toBeDisabled();
        });
    });

    test('should set maxFoodRepeat to 1 when checkbox is unchecked', async () => {
        render(MenuRequestForm);
        const checkbox = screen.getByRole('checkbox');

        await fireEvent.click(checkbox);

        expect(get(menuRequestStore).maxFoodRepeat).toBe(1);
    });

    test('should maxFoodRepeat have a value of null if checkbox is checked ', async () => {
        render(MenuRequestForm);

        expect(get(menuRequestStore).maxFoodRepeat).toBe(null);
    });

    test("sends all params on the api", async () => {
        const mockFoods = [{name: "Mocked Food", kcal: 500}];
        const apiSpy = vi.spyOn(FoodPlannerClient, "getMenuPlan").mockResolvedValue({
            foods: mockFoods,
            foodLogEntry: {chicken: 500, sugar: 200, oil: 10}
        });

        render(MenuRequestForm);

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);

        const callArgs = apiSpy.mock.calls[0][0];
        expect(apiSpy).toHaveBeenCalled();
        expect(callArgs).toHaveProperty("date");
        expect(callArgs).toHaveProperty("foodBlacklist");
        expect(callArgs).toHaveProperty("nutritionalConstraints");
        expect(callArgs).toHaveProperty("maxFoodRepeat");
    });

    test('disables the generate button when at least one macro constraint is invalid', async () => {
        menuRequestStore.set({
            macroConstraints: [
                {name: 'Protein', min: 200, max: 100, unit: 'g', emoji: '🍗'},
                {name: 'Carbs', min: 100, max: 300, unit: 'g', emoji: '🍞'},
            ]
        })

        render(MenuRequestForm);

        const button = screen.getByRole('button', {name: /generate my menu/i});

        expect(button).toBeDisabled();
    });

});
