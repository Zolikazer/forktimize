import {render, screen} from '@testing-library/svelte';
import MaxFoodRepeat from "$lib/components/forms/MaxFoodRepeat.svelte";
import {describe, expect, test} from "vitest";

describe('FoodRepeatCheckbox Component', () => {
    test('initial state has foodCanRepeat as true', () => {
        render(MaxFoodRepeat);
        const checkbox = screen.getByRole('checkbox');

        expect(checkbox).toBeChecked();
    });
});
