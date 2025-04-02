import { render, fireEvent, screen } from "@testing-library/svelte";
import { get } from "svelte/store";
import { mealPlanRequestStore } from "$lib/stores/mealPlanRequestStore.js";
import {FoodProvider, foodProviderList} from "$lib/utils/foodProviders.js";
import FoodProviderSelector from "$lib/components/forms/FoodProviderSelector.svelte";
import {beforeEach, describe, expect, test, vi} from "vitest";


describe("Food Provider Selector", () => {
    test("should render all food provider options", () => {
        render(FoodProviderSelector);
        const select = screen.getByRole("combobox");

        foodProviderList.forEach(({ label }) => {
            expect(select.innerHTML).toContain(label);
        });
    });

    test("should default to CITY_FOOD in store", () => {
        render(FoodProviderSelector);
        expect(get(mealPlanRequestStore).foodProvider).toBe(FoodProvider.CITY_FOOD.value);
    });

    test("should update the store when user selects a different kitchen", async () => {
        render(FoodProviderSelector);
        const select = screen.getByRole("combobox");

        await fireEvent.change(select, { target: { value: FoodProvider.INTER_FOOD.value } });

        expect(get(mealPlanRequestStore).foodProvider).toBe(FoodProvider.INTER_FOOD.value);
    });
});
