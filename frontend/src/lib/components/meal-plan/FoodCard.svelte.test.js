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
        mealPlanStore.setSuccess([mockFood],
            null,
            null,
            mockFood.price,
            mockFood.calories,
            mockFood.protein,
            mockFood.carb,
            mockFood.fat)
        render(FoodCard, {food: mockFood});
        const button = screen.getByText(/Nem szeretem/i);

        await fireEvent.click(button);

        expect(get(mealPlanRequestStore).dislikedFoods).toContain(mockFood.name);
        expect(get(mealPlanStore).foods).toHaveLength(0);
        expect(get(mealPlanStore).totalPrice).toBe(0);
        expect(get(mealPlanStore).totalCalories).toBe(0);
        expect(get(mealPlanStore).totalProtein).toBe(0);
        expect(get(mealPlanStore).totalCarbs).toBe(0);
        expect(get(mealPlanStore).totalFat).toBe(0);
    });

    test('removes all foods with matching name when button is clicked', async () => {
        const duplicateFood1 = { ...mockFood, id: 1, name: "Test Food" };
        const duplicateFood2 = { ...mockFood, id: 2, name: "Test Food" };

        const totalPrice = duplicateFood1.price + duplicateFood2.price;
        const totalCalories = duplicateFood1.calories + duplicateFood2.calories;
        const totalProtein = duplicateFood1.protein + duplicateFood2.protein;
        const totalCarbs = duplicateFood1.carb + duplicateFood2.carb;
        const totalFat = duplicateFood1.fat + duplicateFood2.fat;

        mealPlanStore.setSuccess(
            [duplicateFood1, duplicateFood2],
            null,
            null,
            totalPrice,
            totalCalories,
            totalProtein,
            totalCarbs,
            totalFat
        );

        render(FoodCard, { food: duplicateFood1 });

        const button = screen.getByText(/Nem szeretem/i);
        await fireEvent.click(button);

        expect(get(mealPlanRequestStore).dislikedFoods).toContain(duplicateFood1.name);
        expect(get(mealPlanStore).foods).toHaveLength(0);
        expect(get(mealPlanStore).totalPrice).toBe(0);
        expect(get(mealPlanStore).totalCalories).toBe(0);
        expect(get(mealPlanStore).totalProtein).toBe(0);
        expect(get(mealPlanStore).totalCarbs).toBe(0);
        expect(get(mealPlanStore).totalFat).toBe(0);
    });

});
