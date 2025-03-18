import {fireEvent, render, screen} from "@testing-library/svelte";
import {describe, expect, test, vi} from "vitest";
import Input from "$lib/components/input/Input.svelte";
import {FoodPlannerClient} from "$lib/foodPlannerClient.js";


vi.mock("$lib/stores/menuStore.js", () => {
    return {
        MenuStatusEnum: {
            NOT_GENERATED: "notGenerated",
            IN_PROGRESS: "inProgress",
            SUCCESS: "success",
            FAILURE: "failure"
        },
        menu: {
            set: vi.fn(),
            subscribe: vi.fn().mockImplementation((run) => {
                run([]); // Default: Empty menu
                return {unsubscribe: vi.fn()};
            }),
        },
        currentMenuStatus: {
            set: vi.fn(),
            subscribe: vi.fn().mockImplementation((run) => {
                run("notGenerated"); // Default: No menu generated yet
                return {unsubscribe: vi.fn()};
            }),
        },
    };
});


vi.mock("$lib/foodPlannerClient.js"); // Mock the entire module

describe("Input Component", () => {
    test("renders all macro constraint inputs", () => {
        const {getByText, queryAllByText} = render(Input);

        expect(screen.getByText((content) => content.includes("Calories")));
        expect(screen.getByText((content) => content.includes("Protein")));
        expect(screen.getByText((content) => content.includes("Carb")));
        expect(screen.getByText((content) => content.includes("Fat")));
    });

    test("renders date selector and food blacklist", () => {
        render(Input);

        expect(screen.getByText((content) => content.includes("Select a Date")));
        expect(screen.getByText((content) => content.includes("Foods You Dislike 🤮")));

    });

    test("calls generateMenu() when clicking 'Generate My Menu'", async () => {
        FoodPlannerClient.getMenuPlan.mockResolvedValue({
            data: { foods: [{ name: "Mocked Food", kcal: 500 }] }
        });

        const { component } = render(Input, {
            dates: ["2025-03-10", "2025-03-11", "2025-03-12"],
        });

        const select = screen.getByRole("combobox");
        await fireEvent.change(select, { target: { value: "2025-03-10" } });

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);


        const {menu} = await import("$lib/stores/menuStore.js");
        expect(menu.set).toHaveBeenCalled();


    });
});
