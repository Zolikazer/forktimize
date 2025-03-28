import {render} from '@testing-library/svelte';
import MaxFoodRepeat from "$lib/components/forms/MaxFoodRepeat.svelte";
import {describe, expect, test} from "vitest";

describe('FoodRepeatCheckbox Component', () => {
    test('initial state has foodCanRepeat as true', () => {
        const { getByRole } = render(MaxFoodRepeat);
        const checkbox = getByRole('checkbox');

        expect(checkbox).toBeChecked();
    });
});
