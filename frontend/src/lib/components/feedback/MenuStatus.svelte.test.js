import {beforeEach, describe, expect, test} from 'vitest';
import '@testing-library/jest-dom/vitest';
import {render, screen, waitFor} from '@testing-library/svelte';
import {menuStore} from "$lib/stores/menuStore.js";
import MenuStatus from "$lib/components/feedback/MenuStatus.svelte";

beforeEach(() => {
    menuStore.reset()
});

describe("Menu status Component", () => {
    test("shows success message when menu is available", async () => {
        menuStore.setSuccess();

        render(MenuStatus);

        expect(screen.getByText(/Your menu is ready/i)).toBeInTheDocument();
    });

    test("shows default message when no menu is generated", async () => {
        render(MenuStatus);

        expect(screen.getByText(/No menu generated yet/i)).toBeInTheDocument();
    });

    test("shows in progress message when menu generation is in progress", async () => {
        menuStore.setLoading();

        render(MenuStatus);

        expect(screen.getByText(/Generating your menu/i)).toBeInTheDocument();
    });

    test("shows failure message when could not generate menu", async () => {
        menuStore.setFailure();

        render(MenuStatus);

        expect(screen.getByText(/Sorry, we could not find a menu that meets your needs/i)).toBeInTheDocument();
    });

    test("updates menu status on change", async () => {
        render(MenuStatus);

        expect(screen.getByText(/No menu generated yet/i)).toBeInTheDocument();

        menuStore.setFailure();

        await waitFor(() =>
            expect(screen.getByText(/Sorry, we could not find a menu that meets your needs/i)
            ).toBeInTheDocument()
        );
    });
});
