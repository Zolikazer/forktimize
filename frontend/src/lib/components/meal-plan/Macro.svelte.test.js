import {render} from '@testing-library/svelte';
import Macro from "$lib/components/meal-plan/Macro.svelte";
import {describe, expect, test} from "vitest";


describe('Macro', () => {
    test('renders macro name, value and progress bar correctly', () => {
        const {getByText, container} = render(Macro, {
            props: {
                macroName: 'Protein',
                macroValue: '42',
                macroRatio: '60',
                ratioColorClass: 'has-background-primary'
            }
        });

        // Check for text
        expect(getByText('Protein')).toBeInTheDocument();
        expect(getByText('42g')).toBeInTheDocument();

        // Check the progress bar width
        const fill = container.querySelector('.progress-fill');
        expect(fill).toHaveStyle('width: 60%');
        expect(fill.classList.contains('has-background-primary')).toBe(true);
    });
});
