import { render, screen, fireEvent } from "@testing-library/svelte";
import { expect, test, describe } from "vitest";
import DateSelector from "$lib/components/input/DateSelector.svelte";

describe("DateSelector", () => {
    const mockDates = ["2025-03-10", "2025-03-11", "2025-03-12"];

    test("renders dropdown with correct dates", () => {
        render(DateSelector, { dates: mockDates, selectedDate: mockDates[0] });

        const select = screen.getByLabelText("Select a Date 📅");
        expect(select).toBeInTheDocument();

        mockDates.forEach((date) => {
            expect(screen.getByText(new RegExp(date))).toBeInTheDocument();
        });
    });

    test("displays formatted date labels", () => {
        render(DateSelector, { dates: mockDates, selectedDate: mockDates[0] });

        mockDates.forEach((date) => {
            const formattedLabel = `${date} | ${new Date(date).toLocaleDateString("en-US", { weekday: "long" })}`;
            expect(screen.getByText(formattedLabel)).toBeInTheDocument();
        });
    });

    test("updates selected date when user selects a new one", async () => {
        render(DateSelector, { dates: mockDates, selectedDate: mockDates[0] });

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, { target: { value: mockDates[1] } });

        // ✅ This is the correct way to verify the change!
        expect(select.value).toBe(mockDates[1]);
    });

    test("handles empty dates array gracefully", () => {
        render(DateSelector, { dates: [] });

        const select = screen.getByLabelText("Select a Date 📅");
        expect(select).toBeInTheDocument();
        expect(select.children.length).toBe(0); // No options should exist
    });

    test("defaults to the first available date if selectedDate is not provided", () => {
        render(DateSelector, { dates: mockDates });

        const select = screen.getByRole("combobox");
        expect(select.value).toBe(mockDates[0]); // Should default to first date
    });
});
