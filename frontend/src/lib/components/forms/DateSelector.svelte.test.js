import {fireEvent, render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test, vi} from "vitest";
import DateSelector from "$lib/components/forms/DateSelector.svelte";
import {vendorListStore} from "$lib/stores/foodVendorStore.js";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";

const mockDates = ["2025-03-10", "2025-03-11", "2025-03-12"];


describe("DateSelector", () => {
    test("renders dropdown with correct dates", async () => {
        render(DateSelector, {
            props: { dates: mockDates, selectedDate: mockDates[0] },
        });
        await screen.findByText(/2025-03-10/i);

        const select = screen.getByLabelText(/Select Date/i);
        expect(select).toBeInTheDocument();

        mockDates.forEach((date) => {
            expect(screen.getByText(new RegExp(date))).toBeInTheDocument();
        });
    });

    test("displays formatted date labels", async () => {
        render(DateSelector, {
            props: { dates: mockDates, selectedDate: mockDates[0] },
        });

        await screen.findByText(/2025-03-10/i);

        mockDates.forEach((date) => {
            const formattedLabel = `${date} | ${new Date(date).toLocaleDateString("en-US", {weekday: "long"})}`;
            expect(screen.getByText(formattedLabel)).toBeInTheDocument();
        });
    });

    test("updates selected date when user selects a new one", async () => {
        const initialDate = mockDates[0];
        const dateToSelect = mockDates[1];
        render(DateSelector, {
            props: { dates: mockDates, selectedDate: initialDate },
        });

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: dateToSelect}});

        expect(select.value).toBe(dateToSelect);
    });

});
