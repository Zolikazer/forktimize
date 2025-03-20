import {fireEvent, render, screen} from "@testing-library/svelte";
import {describe, expect, test, vi, beforeEach} from "vitest";
import Input from "$lib/components/input/Input.svelte";
import {FoodPlannerClient} from "$lib/foodPlannerClient.js";
import {menu, currentMenuStatus, MenuStatusEnum} from "$lib/stores/menuStore.js";
import {get} from "svelte/store";


beforeEach(() => {
    menu.set([]);
    currentMenuStatus.set(MenuStatusEnum.NOT_GENERATED);
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
        const generatedMenu = {name: "Mocked Food", kcal: 500};
        FoodPlannerClient.getMenuPlan.mockResolvedValue({
            data: {foods: [generatedMenu]}
        });

        render(Input, {dates: ["2025-03-10", "2025-03-11", "2025-03-12"],});

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, {target: {value: "2025-03-10"}});

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);

        expect(get(menu)).toEqual([generatedMenu]);
    });
});
