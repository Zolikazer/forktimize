import {describe, expect, test} from 'vitest';
import '@testing-library/jest-dom/vitest';
import {render, screen} from '@testing-library/svelte';
import {menuStatus, MenuGenerationStatus} from "$lib/stores/menuStore.js";
import MenuStatusDisplay from "$lib/components/help/MenuStatusDisplay.svelte";


describe("Menu status Component", () => {
    test("shows success message when menu is available", async () => {
        menuStatus.set(MenuGenerationStatus.SUCCESS);

        render(MenuStatusDisplay);

        expect(screen.getByText(/Your menu is ready/i)).toBeInTheDocument();
    });

    test("shows default message when no menu is generated", async () => {
        menuStatus.set(MenuGenerationStatus.NOT_GENERATED);

        render(MenuStatusDisplay);

        expect(screen.getByText(/No menu generated yet/i)).toBeInTheDocument();
    });

    test("shows in progress message when menu generation is in progress", async () => {
        menuStatus.set(MenuGenerationStatus.IN_PROGRESS);

        render(MenuStatusDisplay);

        expect(screen.getByText(/Generating your menu/i)).toBeInTheDocument();
    });

    test("shows failure message when could not generate menu", async () => {
        menuStatus.set(MenuGenerationStatus.FAILURE);

        render(MenuStatusDisplay);

        expect(screen.getByText(/Sorry, we could not find a menu that meets your needs/i)).toBeInTheDocument();
    });
});
