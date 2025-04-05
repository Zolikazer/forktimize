import {fireEvent, render, screen} from '@testing-library/svelte';
import {get} from 'svelte/store';
import FoodBlacklist from '$lib/components/forms/FoodBlacklist.svelte';
import {beforeEach, describe, expect, test} from 'vitest';
import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";


beforeEach(() => {
    mealPlanRequestStore.set({selectedDate: null, macroConstraints: [], dislikedFoods: []});
});

describe('FoodBlacklist component', () => {
    test('renders the component with empty blacklist', () => {
        render(FoodBlacklist);

        expect(screen.getByText(/Foods You Dislike/i)).toBeInTheDocument();
        expect(screen.queryAllByText(/\w+/).length).toBe(1);
    });

    test('adds a food to the blacklist when pressing Enter', async () => {
        render(FoodBlacklist);
        const input = screen.getByPlaceholderText('Type a food and press Enter');

        await fireEvent.input(input, {target: {value: 'Broccoli'}});
        await fireEvent.keyDown(input, {key: 'Enter'});

        expect(get(mealPlanRequestStore).dislikedFoods).toContain('Broccoli');
        expect(input.value).toBe('');
    });

    test('removes a food from blacklist when clicking delete button', async () => {
        mealPlanRequestStore.addDislikedFood('Spinach');
        render(FoodBlacklist);

        const deleteButton = screen.getByRole("button");
        await fireEvent.click(deleteButton);

        expect(get(mealPlanRequestStore).dislikedFoods).not.toContain('Spinach');
    });

    test('does not add empty food names to the blacklist', async () => {
        render(FoodBlacklist);
        const input = screen.getByPlaceholderText(/Type a food and press Enter/i);

        await fireEvent.input(input, {target: {value: '   '}});
        await fireEvent.keyDown(input, {key: 'Enter'});

        expect(get(mealPlanRequestStore).dislikedFoods.length).toBe(0);
    });

    test('shortens long food names in the display', async () => {
        mealPlanRequestStore.addDislikedFood('VeryLongFoodNameThatShouldBeTruncated');
        render(FoodBlacklist);

        expect(screen.getByText('VeryLong...')).toBeInTheDocument();
    });

    test('adds food when clicking outside the forms', async () => {
        render(FoodBlacklist);
        const input = screen.getByPlaceholderText(/Type a food and press Enter/i);

        await fireEvent.input(input, {target: {value: 'Kale'}});
        await fireEvent.click(document.body);

        expect(get(mealPlanRequestStore).dislikedFoods).toContain('Kale');
    });
});
