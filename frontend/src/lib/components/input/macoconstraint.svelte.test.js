import {fireEvent, render} from '@testing-library/svelte';
import MacroConstraint from '$lib/components/input/MacroConstraint.svelte';
import {describe, expect, test} from 'vitest';

describe('MacroConstraint component', () => {
    test('renders with provided props', () => {
        const {getByText} = render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100,
            unit: 'g',
            emoji: '💪'
        });

        expect(getByText('Protein (g) 💪')).toBeInTheDocument();
        expect(getByText('Min')).toBeInTheDocument();
        expect(getByText('Max')).toBeInTheDocument();
    });

    test('handles negative values by resetting to empty', async () => {
        const {getAllByRole} = render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100
        });

        const inputs = getAllByRole('spinbutton');
        const minInput = inputs[0];

        await fireEvent.input(minInput, {target: {value: -10}});
        await fireEvent.blur(minInput);

        expect(minInput.value).toBe('');
    });

    test('validates max is not less than min', async () => {
        const {getAllByRole} = render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100
        });

        const inputs = getAllByRole('spinbutton');
        const minInput = inputs[0];
        const maxInput = inputs[1];

        // Set min higher than max
        await fireEvent.input(minInput, {target: {value: 120}});
        await fireEvent.blur(minInput);

        // Check that validation class is applied
        expect(minInput).toHaveClass('is-danger');
        expect(maxInput).toHaveClass('is-danger');

        // Now fix the validation by setting max higher
        await fireEvent.input(maxInput, {target: {value: 150}});
        await fireEvent.blur(maxInput);

        // Check that validation error is gone
        expect(minInput).not.toHaveClass('is-danger');
        expect(maxInput).not.toHaveClass('is-danger');
    });

    test('tooltip containers have correct classes when invalid', async () => {
        const {getAllByRole, container} = render(MacroConstraint, {
            label: 'Protein',
            minValue: 100,
            maxValue: 50  // Intentionally invalid
        });

        const inputs = getAllByRole('spinbutton');
        const minInput = inputs[0];

        // Trigger validation
        await fireEvent.blur(minInput);

        // Check that tooltip containers have has-tooltip class
        const tooltipContainers = container.querySelectorAll('.tooltip-container');
        expect(tooltipContainers[0]).toHaveClass('has-tooltip');
        expect(tooltipContainers[1]).toHaveClass('has-tooltip');
    });

    test('validates NaN inputs by resetting to empty', async () => {
        const {getAllByRole} = render(MacroConstraint, {
            label: 'Protein',
            minValue: '',
            maxValue: 100
        });

        const inputs = getAllByRole('spinbutton');
        const minInput = inputs[0];

        // This will convert to NaN for the number input
        await fireEvent.input(minInput, {target: {value: 'abc'}});
        await fireEvent.blur(minInput);

        expect(minInput.value).toBe('');
    });
});
