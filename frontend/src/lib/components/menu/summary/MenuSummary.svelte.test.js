import {render, screen} from '@testing-library/svelte';
import {beforeEach, describe, expect, test} from 'vitest';
import {menuStore} from '$lib/stores/menuStore.js';
import MenuSummary from "$lib/components/menu/summary/MenuSummary.svelte";

beforeEach(() => {
    menuStore.setSuccess([
        {
            name: 'Test Food 1',
            calories: 300,
            protein: 20,
            carb: 40,
            fat: 10,
            price: 1500
        },
        {
            name: 'Test Food 2',
            calories: 400,
            protein: 25,
            carb: 50,
            fat: 15,
            price: 2000
        }
    ]);
});

describe('MenuSummarySvelte Component', () => {
    test('renders title correctly', () => {
        render(MenuSummary);
        expect(screen.getByText(/Meal Plan Summary/i)).toBeInTheDocument();
    });

    test('calculates and displays total cost correctly', () => {
        render(MenuSummary);
        expect(screen.getByText(/3 500 Ft/)).toBeInTheDocument();
    });

    test('calculates and displays total calories correctly', () => {
        render(MenuSummary);
        expect(screen.getByText(/700 calories/)).toBeInTheDocument();
    });

    test('calculates and displays macronutrients correctly', () => {
        render(MenuSummary);

        expect(screen.getByText(/45 g/i)).toBeInTheDocument();
        expect(screen.getByText(/90 g/i)).toBeInTheDocument();
        expect(screen.getByText(/25 g/i)).toBeInTheDocument();
    });
});
