import {fireEvent, render, screen} from "@testing-library/svelte";
import {describe, expect, test} from "vitest";
import DateSelector from "$lib/components/forms/DateSelector.svelte";

const mockDates = ["2025-03-10", "2025-03-11", "2025-03-12"];


describe("DateSelector", () => {
    test("renders dropdown with correct dates", async () => {
        render(DateSelector, {
            props: { dates: mockDates, selectedDate: mockDates[0] },
        });

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

    test("shows loading spinner when dates are initially null or empty", () => {
        render(DateSelector, {
            props: { dates: [] },
        });

        const selectElement = screen.getByRole("combobox");
        const selectWrapper = selectElement.closest('div.select');
        expect(selectWrapper).toHaveClass('is-loading');
    });

    test("it does not show loading spinner if dates is not empty", () => {
        render(DateSelector, {
            props: { dates: mockDates },
        });

        const selectElement = screen.getByRole("combobox");
        const selectWrapper = selectElement.closest('div.select');
        expect(selectWrapper).not.toHaveClass('is-loading');
    });

});
