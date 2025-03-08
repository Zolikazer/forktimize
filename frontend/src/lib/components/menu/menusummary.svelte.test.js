import {render, screen} from '@testing-library/svelte';
import {describe, expect, test, vi} from 'vitest';
import MenuSummary from '$lib/components/menu/MenuSummary.svelte';

// Mock the menu store
vi.mock('$lib/stores/menuStore.js', () => {
    const mockMenu = [
        {
            name: 'Test Food 1',
            kcal: 300,
            protein: 20,
            carbs: 40,
            fat: 10,
            price: 1500
        },
        {
            name: 'Test Food 2',
            kcal: 400,
            protein: 25,
            carbs: 50,
            fat: 15,
            price: 2000
        }
    ];

    return {
        menu: {
            subscribe: vi.fn(callback => {
                callback(mockMenu);
                return {unsubscribe: vi.fn()};
            })
        }
    };
});

describe('MenuSummary Component', () => {
    test('renders title correctly', () => {
        render(MenuSummary);

        expect(screen.getByText('Menu Summary')).toBeInTheDocument();
    });

    test('calculates and displays total cost correctly', () => {
        render(MenuSummary);

        expect(screen.getByText(/3 500 Ft/)).toBeInTheDocument();
    });

    test('calculates and displays total calories correctly', () => {
        render(MenuSummary);

        expect(screen.getByText(/700 kcal/)).toBeInTheDocument();
    });

    test('calculates and displays macronutrients correctly', () => {
        render(MenuSummary);

        expect(screen.getByText((content) => content.includes("45 g")));

        expect(screen.getByText((content) => content.includes("90 g")));

        expect(screen.getByText((content) => content.includes("25 g")));

    });

});
