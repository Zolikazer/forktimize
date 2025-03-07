import {describe, expect, test} from 'vitest';
import '@testing-library/jest-dom/vitest';
import {render, screen} from '@testing-library/svelte';
import {menu} from "$lib/stores/menuStore.js";
import Help from "$lib/components/help/Help.svelte";


describe("Help Component", () => {
    test("shows success message when menu is available", async () => {
        menu.set([{name: "Food Item"}]); // Mock menu with data

        render(Help);

        expect(screen.getByText("Your menu is ready. ✅")).toBeInTheDocument();
    });

    test("shows default message when no menu is generated", async () => {
        menu.set(null); // Mock menu with data

        render(Help);

        expect(screen.getByText(/No menu generated yet/i)).toBeInTheDocument();
    });
});
