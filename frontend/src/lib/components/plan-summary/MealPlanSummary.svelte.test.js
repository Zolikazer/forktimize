import {render, screen} from '@testing-library/svelte';
import {beforeEach, describe, expect, test} from 'vitest';
import {mealPlanStore} from '$lib/stores/mealPlanStore.js';
import MealPlanSummary from "$lib/components/plan-summary/MealPlanSummary.svelte";

beforeEach(() => {
    mealPlanStore.setSuccess(
        [
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
        ],
        null,
        "2025-05-06",
        1500,
        1600,
        200,
        100,
        30);
});

describe('MealPlanSummarySvelte Component', () => {
    test('renders title correctly', () => {
        render(MealPlanSummary);
        expect(screen.getByText(/Meal Plan Summary/i)).toBeInTheDocument();
    });

    test('calculates and displays total cost correctly', () => {
        render(MealPlanSummary);
        expect(screen.getByText(/1 500 Ft/)).toBeInTheDocument();
    });

    test('calculates and displays total calories correctly', () => {
        render(MealPlanSummary);
        expect(screen.getByText(/1 600 calories/)).toBeInTheDocument();
    });

    test('calculates and displays macronutrients correctly', () => {
        render(MealPlanSummary);

        expect(screen.getByText(/200 g/i)).toBeInTheDocument();
        expect(screen.getByText(/100 g/i)).toBeInTheDocument();
        expect(screen.getByText(/30 g/i)).toBeInTheDocument();
    });

    test('displays date properly', () => {
        render(MealPlanSummary);
        expect(screen.getByText(/2025. május 6., kedd/i)).toBeInTheDocument();
    });
});
