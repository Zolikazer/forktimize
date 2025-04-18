import {fireEvent, render, screen} from "@testing-library/svelte";
import {get} from "svelte/store";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
import {FoodVendor, foodVendorList} from "$lib/utils/foodVendors.js";
import FoodVendorSelector from "$lib/components/forms/FoodVendorSelector.svelte";
import {beforeEach, describe, expect, test} from "vitest";
import {vendorListStore} from "$lib/stores/foodVendorStore.js";

beforeEach(() => {
    vendorListStore.set([]);
});
const VENDORS = [{name: "CityFood", type: "cityfood"}, {name: "interfood", type: "interfood"}];

describe("Food Vendor Selector", () => {
    test("should render all food vendor options", () => {
        vendorListStore.set(VENDORS);
        render(FoodVendorSelector);
        const select = screen.getByRole("combobox");

        VENDORS.forEach((vendor) => {
            expect(select.innerHTML).toContain(vendor.name);
        });
    });

    test("should default to CITY_FOOD in store", () => {
        render(FoodVendorSelector);
        expect(get(mealPlanRequestStore).foodVendor).toBe(FoodVendor.CITY_FOOD.value);
    });

    test("should update the store when user selects a different kitchen", async () => {
        vendorListStore.set(VENDORS);
        render(FoodVendorSelector);
        const select = screen.getByRole("combobox");

        await fireEvent.change(select, {target: {value: FoodVendor.INTER_FOOD.value}});

        expect(get(mealPlanRequestStore).foodVendor).toBe(FoodVendor.INTER_FOOD.value);
    });
});
