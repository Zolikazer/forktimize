import {render, screen, fireEvent} from "@testing-library/svelte";
import {expect, test, describe, vi, beforeEach} from "vitest";
import * as FoodPlannerClient from "$lib/api/foodPlannerApi.js";
import DateSelector from "$lib/components/forms/DateSelector.svelte";
import {vendorListStore} from "$lib/stores/foodVendorStore.js";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";

const mockDates = ["2025-03-10", "2025-03-11", "2025-03-12"];

beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(FoodPlannerClient, "getDates").mockResolvedValue(mockDates);
    vendorListStore.set([])
    mealPlanRequestStore.reset()

});

describe("DateSelector", () => {
    test("renders dropdown with correct dates", async () => {
        vendorListStore.set([{type: "vendor", availableDates: mockDates}])
        mealPlanRequestStore.setVendor("vendor")
        render(DateSelector);
        await screen.findByText(/2025-03-10/i);

        const select = screen.getByLabelText(/Select Date/i);
        expect(select).toBeInTheDocument();

        mockDates.forEach((date) => {
            expect(screen.getByText(new RegExp(date))).toBeInTheDocument();
        });
    });

    test("displays formatted date labels", async () => {
        vendorListStore.set([{type: "vendor", availableDates: mockDates}])
        mealPlanRequestStore.setVendor("vendor")
        render(DateSelector);
        await screen.findByText(/2025-03-10/i);

        mockDates.forEach((date) => {
            const formattedLabel = `${date} | ${new Date(date).toLocaleDateString("en-US", {weekday: "long"})}`;
            expect(screen.getByText(formattedLabel)).toBeInTheDocument();
        });
    });

    test("updates selected date when user selects a new one", async () => {
        vendorListStore.set([{type: "vendor", availableDates: mockDates}])
        mealPlanRequestStore.setVendor("vendor")
        render(DateSelector);
        await screen.findByText(/2025-03-10/i);

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: mockDates[1]}});

        expect(select.value).toBe(mockDates[1]);
    });

    test("defaults to the first available date if selectedDate is not provided", async () => {
        vendorListStore.set([{type: "vendor", availableDates: mockDates}])
        mealPlanRequestStore.setVendor("vendor")
        render(DateSelector);
        await screen.findByText(/2025-03-10/i);


        const select = screen.getByRole("combobox");
        expect(select.value).toBe(mockDates[0]);
    });
});
