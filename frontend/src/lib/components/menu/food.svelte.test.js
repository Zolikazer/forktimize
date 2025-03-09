import {fireEvent, render} from '@testing-library/svelte';
import Food from '$lib/components/menu/Food.svelte';
import {dislikedFoods} from "$lib/stores/dislikedFoodsStore.js";
import {menu} from "$lib/stores/menuStore.js";
import {beforeEach, describe, expect, test, vi} from 'vitest';

// Mock the stores
vi.mock("$lib/stores/dislikedFoodsStore.js", () => ({
    dislikedFoods: {
        subscribe: vi.fn(),
        update: vi.fn()
    }
}));

vi.mock("$lib/stores/menuStore.js", () => ({
    menu: {
        subscribe: vi.fn(),
        update: vi.fn()
    }
}));

describe('Food component', () => {
    const mockFood = {
        name: "Test Food Item",
        calories: 300,
        protein: 20,
        carb: 40,
        fat: 10,
        price: 1500
    };

    const mockLongNameFood = {
        name: "This is a very long food name that exceeds the maximum length and should be truncated",
        calories: 400,
        protein: 25,
        carb: 50,
        fat: 15,
        price: 2000
    };

    beforeEach(() => {
        vi.resetAllMocks();
    });

    test('renders food information correctly', () => {
        const {getByText, getByAltText} = render(Food, {food: mockFood});

        expect(getByText(mockFood.name)).toBeInTheDocument();
        expect(getByText(`${mockFood.price} Ft`)).toBeInTheDocument();
        expect(getByText(`🔥 ${mockFood.calories}`)).toBeInTheDocument();
        expect(getByText(`💪 ${mockFood.protein}`)).toBeInTheDocument();
        expect(getByText(`🥖 ${mockFood.carb}`)).toBeInTheDocument();
        expect(getByText(`🧈️ ${mockFood.fat}`)).toBeInTheDocument();
        expect(getByAltText('Placeholder image')).toBeInTheDocument();
        expect(getByText('🤮 Nem szeretem')).toBeInTheDocument();
    });

    test('truncates long food names', () => {
        const {getByText} = render(Food, {food: mockLongNameFood});

        const truncatedName = mockLongNameFood.name.substring(0, 42) + "...";
        expect(getByText(truncatedName)).toBeInTheDocument();
    });

    test('displays full name in tooltip data attribute', () => {
        const {container} = render(Food, {food: mockLongNameFood});

        const foodNameElement = container.querySelector('.food-name');
        expect(foodNameElement).toHaveAttribute('data-tooltip', mockLongNameFood.name);
    });

    test('removes food when button is clicked', async () => {
        const {getByText} = render(Food, {food: mockFood});
        const button = getByText('🤮 Nem szeretem');

        await fireEvent.click(button);

        expect(dislikedFoods.update).toHaveBeenCalled();
        expect(menu.update).toHaveBeenCalled();

        // Extract the function passed to dislikedFoods.update
        const dislikedFoodsUpdateFn = dislikedFoods.update.mock.calls[0][0];
        const updatedDislikedFoods = dislikedFoodsUpdateFn([]);
        expect(updatedDislikedFoods).toContain(mockFood.name);

        // Extract the function passed to menu.update
        const menuUpdateFn = menu.update.mock.calls[0][0];
        const updatedMenu = menuUpdateFn([mockFood]);
        expect(updatedMenu).toHaveLength(0);
    });

});
