import {beforeEach, describe, expect, test} from 'vitest';
import '@testing-library/jest-dom/vitest';
import {render, screen, waitFor} from '@testing-library/svelte';
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
import MealPlanStatus from "$lib/components/feedback/MealPlanStatus.svelte";

beforeEach(() => {
    mealPlanStore.reset()
});

describe("Meal Plan status Component", () => {
    test("shows success message when meal plan is available", async () => {
        mealPlanStore.setSuccess();

        render(MealPlanStatus);

        expect(screen.getByText(/Your meal plan is ready/i)).toBeInTheDocument();
    });

    test("shows default message when no meal plan is generated", async () => {
        render(MealPlanStatus);

        expect(screen.getByText(/No meal plan generated yet/i)).toBeInTheDocument();
    });

    test("shows in progress message when meal plan generation is in progress", async () => {
        mealPlanStore.setLoading();

        render(MealPlanStatus);

        expect(screen.getByText(/Generating your meal plan/i)).toBeInTheDocument();
    });

    test("shows failure message when could not generate meal plan", async () => {
        mealPlanStore.setFailure();

        render(MealPlanStatus);

        expect(screen.getByText(/Sorry, we could not find a meal plan that meets your needs/i)).toBeInTheDocument();
    });

    test("updates meal plan status on change", async () => {
        render(MealPlanStatus);

        expect(screen.getByText(/No meal plan generated yet/i)).toBeInTheDocument();

        mealPlanStore.setFailure();

        await waitFor(() =>
            expect(screen.getByText(/Sorry, we could not find a meal plan that meets your needs/i)
            ).toBeInTheDocument()
        );
    });
});
