import {fireEvent, render} from '@testing-library/svelte';
import {get} from 'svelte/store';
import FoodBlacklist from '$lib/components/input/FoodBlacklist.svelte';
import {dislikedFoods} from '$lib/stores/dislikedFoodsStore.js';
import {describe, expect, test, beforeEach} from 'vitest';


// Reset store between tests
beforeEach(() => {
    dislikedFoods.set([]);
});

describe('FoodBlacklist component', () => {
    test('renders the component with empty blacklist', () => {
        const { getByText, queryAllByText } = render(FoodBlacklist);

        expect(getByText('Foods You Dislike 🤮')).toBeInTheDocument();
        expect(queryAllByText(/\w+/).length).toBe(1); // Only the label text
    });

    test('adds a food to the blacklist when pressing Enter', async () => {
        const { getByPlaceholderText } = render(FoodBlacklist);
        const input = getByPlaceholderText('Type a food and press Enter');

        await fireEvent.input(input, { target: { value: 'Broccoli' } });
        await fireEvent.keyDown(input, { key: 'Enter' });

        expect(get(dislikedFoods)).toContain('Broccoli');
        expect(input.value).toBe(''); // Input cleared after adding
    });

    test('removes a food from blacklist when clicking delete button', async () => {
        // Add a food first
        dislikedFoods.set(['Spinach']);
        const { getByText, getByRole } = render(FoodBlacklist);

        const deleteButton = getByRole("button");
        await fireEvent.click(deleteButton);

        expect(get(dislikedFoods)).not.toContain('Spinach');
    });

    test('does not add empty food names to the blacklist', async () => {
        const { getByPlaceholderText } = render(FoodBlacklist);
        const input = getByPlaceholderText('Type a food and press Enter');

        await fireEvent.input(input, { target: { value: '   ' } });
        await fireEvent.keyDown(input, { key: 'Enter' });

        expect(get(dislikedFoods).length).toBe(0);
    });

    test('shortens long food names in the display', async () => {
        dislikedFoods.set(['VeryLongFoodNameThatShouldBeTruncated']);
        const { getByText } = render(FoodBlacklist);

        expect(getByText('VeryLong...')).toBeInTheDocument();
    });

    test('adds food when clicking outside the input', async () => {
        const { getByPlaceholderText } = render(FoodBlacklist);
        const input = getByPlaceholderText('Type a food and press Enter');

        await fireEvent.input(input, { target: { value: 'Kale' } });
        // Simulate clicking outside
        await fireEvent.click(document.body);

        expect(get(dislikedFoods)).toContain('Kale');
    });
});
