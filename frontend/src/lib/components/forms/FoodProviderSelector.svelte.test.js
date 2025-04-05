import {fireEvent, render, screen} from "@testing-library/svelte";
import {get} from "svelte/store";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
import {FoodVendor, foodVendorList} from "$lib/utils/foodVendors.js";
import FoodVendorSelector from "$lib/components/forms/FoodVendorSelector.svelte";
import {describe, expect, test} from "vitest";


describe("Food Vendor Selector", () => {
    test("should render all food vendor options", () => {
        render(FoodVendorSelector);
        const select = screen.getByRole("combobox");

        foodVendorList.forEach(({ label }) => {
            expect(select.innerHTML).toContain(label);
        });
    });

    test("should default to CITY_FOOD in store", () => {
        render(FoodVendorSelector);
        expect(get(mealPlanRequestStore).foodVendor).toBe(FoodVendor.CITY_FOOD.value);
    });

    test("should update the store when user selects a different kitchen", async () => {
        render(FoodVendorSelector);
        const select = screen.getByRole("combobox");

        await fireEvent.change(select, { target: { value: FoodVendor.INTER_FOOD.value } });

        expect(get(mealPlanRequestStore).foodVendor).toBe(FoodVendor.INTER_FOOD.value);
    });
});
