import {render, screen} from "@testing-library/svelte";
import {describe, expect, test, vi} from "vitest";
import {menu} from "$lib/stores/menuStore.js";
import Help from "$lib/components/help/Help.svelte";


vi.mock("$lib/stores/menuStore.js", () => ({
    menu: {
        subscribe: vi.fn((fn) => {
            fn(null); // Default state
            return () => {};
        }),
    },
}));

describe("MenuStatusComponent", () => {
    test("displays 'No menu generated yet' when menu is null", () => {
        render(Help);
        expect(screen.getByText(/No menu generated yet/i)).toBeInTheDocument();
    });

    test("displays 'Your menu is ready' when menu has items", () => {
        vi.mocked(menu.subscribe).mockImplementation((fn) => {
            fn([{ name: "Example Item" }]); // Mocking menu with data
            return () => {};
        });

        render(Help);
        expect(screen.getByText(/Your menu is ready/i)).toBeInTheDocument();
    });

    test("displays 'Sorry, we could not find a menu' when menu is empty", () => {
        vi.mocked(menu.subscribe).mockImplementation((fn) => {
            fn([]); // Empty menu state
            return () => {};
        });

        render(Help);
        expect(screen.getByText(/Sorry, we could not find a menu/i)).toBeInTheDocument();
    });
});
