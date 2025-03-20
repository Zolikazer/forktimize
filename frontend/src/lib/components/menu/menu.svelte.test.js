import {render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test} from "vitest";
import Menu from "$lib/components/menu/Menu.svelte";
import {menu} from "$lib/stores/menuStore.js";

beforeEach(() => {
    menu.set([
        {
            name: "Test Food 1",
            calories: 300,
            protein: 20,
            carb: 40,
            fat: 10,
            price: 1500
        },
        {
            name: "Test Food 2",
            calories: 400,
            protein: 25,
            carb: 50,
            fat: 15,
            price: 2000
        }
    ]);
});

describe("Menu Component", () => {
    test("renders title correctly", () => {
        render(Menu);
        expect(screen.getByText(/Your Menu For/i)).toBeInTheDocument();
    });

    test("renders a Food component for each item in the menu", () => {
        const {container} = render(Menu);
        const foodComponents = container.querySelectorAll('.food-card');
        expect(foodComponents.length).toBe(2);
    });
});
