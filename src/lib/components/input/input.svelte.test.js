import {fireEvent, render, screen} from "@testing-library/svelte";
import {describe, expect, test, vi} from "vitest";
import Input from "$lib/components/input/Input.svelte";


vi.mock("$lib/stores/menuStore.js", () => {
    return {
        menu: {
            set: vi.fn(),
            subscribe: vi.fn().mockImplementation((run) => {
                run([]); // Default: Empty menu
                return {unsubscribe: vi.fn()};
            }),
        },
    };
});

describe("Input Component", () => {
    test("renders all macro constraint inputs", () => {
        const {getByText, queryAllByText} = render(Input);

        expect(screen.getByText((content) => content.includes("Calories")));
        expect(screen.getByText((content) => content.includes("Protein")));
        expect(screen.getByText((content) => content.includes("Carbs")));
        expect(screen.getByText((content) => content.includes("Fats")));
    });

    test("renders date selector and food blacklist", () => {
        render(Input);

        expect(screen.getByText((content) => content.includes("Select a Date")));
        expect(screen.getByText((content) => content.includes("Foods You Dislike 🤮")));

    });

    test("calls generateMenu() when clicking 'Generate My Menu'", async () => {
        render(Input);

        const button = screen.getByRole("button", {name: /Generate My Menu/i});
        await fireEvent.click(button);

        const {menu} = await import("$lib/stores/menuStore.js");
        expect(menu.set).toHaveBeenCalled(); // ✅ Ensure `menu.set()` was t
    });
});
