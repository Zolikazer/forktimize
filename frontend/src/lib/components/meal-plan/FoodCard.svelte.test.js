import {fireEvent, render, screen} from '@testing-library/svelte';
import FoodCard from '$lib/components/meal-plan/FoodCard.svelte';
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
import {beforeEach, describe, expect, test} from 'vitest';
import {get} from "svelte/store";
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";

beforeEach(() => {
    mealPlanStore.reset();
    mealPlanRequestStore.set({dislikedFoods: []})
});

describe('FoodCard component', () => {
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

    test('renders food information correctly', () => {
        render(FoodCard, {food: mockFood});

        expect(screen.getByText(mockFood.name)).toBeInTheDocument();
        expect(screen.getByText(`${mockFood.price} Ft`)).toBeInTheDocument();
        expect(screen.getByText(`${mockFood.calories}`)).toBeInTheDocument();
        expect(screen.getByText(`${mockFood.protein}g`)).toBeInTheDocument();
        expect(screen.getByText(`${mockFood.carb}g`)).toBeInTheDocument();
        expect(screen.getByText(`${mockFood.fat}g`)).toBeInTheDocument();
        expect(screen.getByAltText(mockFood.name)).toBeInTheDocument();
        expect(screen.getByText(/Nem szeretem/i)).toBeInTheDocument();
    });

    test('truncates long food names', () => {
        render(FoodCard, {food: mockLongNameFood});

        const truncatedName = mockLongNameFood.name.substring(0, 42) + "...";
        expect(screen.getByText(truncatedName)).toBeInTheDocument();
    });

    test('displays full name in tooltip data attribute', () => {
        const {container} = render(FoodCard, {food: mockLongNameFood});

        const foodNameElement = container.querySelector('.food-name');
        expect(foodNameElement).toHaveAttribute('data-tooltip', mockLongNameFood.name);
    });

    test('removes food when button is clicked', async () => {
        mealPlanStore.setSuccess([mockFood])
        render(FoodCard, {food: mockFood});
        const button = screen.getByText(/Nem szeretem/i);

        await fireEvent.click(button);

        expect(get(mealPlanRequestStore).dislikedFoods).toContain(mockFood.name);
        expect(get(mealPlanStore).foods).toHaveLength(0);
    });
});
