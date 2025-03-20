import {fireEvent, render, screen} from '@testing-library/svelte';
import MacroConstraint from '$lib/components/input/MacroConstraint.svelte';
import {describe, expect, test} from 'vitest';

describe('MacroConstraint component', () => {
    test('renders with provided props', () => {
        render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100,
            unit: 'g',
            emoji: '💪'
        });

        expect(screen.getByText(/Protein/i)).toBeInTheDocument();
        expect(screen.getByText(/Min/i)).toBeInTheDocument();
        expect(screen.getByText(/Max/i)).toBeInTheDocument();
    });

    test('handles negative values by resetting to empty', async () => {
        render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100
        });

        const inputs = screen.getAllByRole('spinbutton');
        const minInput = inputs[0];

        await fireEvent.input(minInput, { target: { value: -10 } });
        await fireEvent.blur(minInput);

        expect(minInput.value).toBe('');
    });

    test('validates max is not less than min', async () => {
        render(MacroConstraint, {
            label: 'Protein',
            minValue: 50,
            maxValue: 100
        });

        const inputs = screen.getAllByRole('spinbutton');
        const minInput = inputs[0];
        const maxInput = inputs[1];

        await fireEvent.input(minInput, { target: { value: 120 } });
        await fireEvent.blur(minInput);

        expect(minInput).toHaveClass('is-danger');
        expect(maxInput).toHaveClass('is-danger');

        await fireEvent.input(maxInput, { target: { value: 150 } });
        await fireEvent.blur(maxInput);

        expect(minInput).not.toHaveClass('is-danger');
        expect(maxInput).not.toHaveClass('is-danger');
    });

    test('tooltip containers have correct classes when invalid', async () => {
        const { container } = render(MacroConstraint, {
            label: 'Protein',
            minValue: 100,
            maxValue: 50
        });

        const inputs = screen.getAllByRole('spinbutton');
        const minInput = inputs[0];

        await fireEvent.blur(minInput);

        const tooltipContainers = container.querySelectorAll('.tooltip-container');
        expect(tooltipContainers[0]).toHaveClass('has-tooltip');
        expect(tooltipContainers[1]).toHaveClass('has-tooltip');
    });

    test('validates NaN inputs by resetting to empty', async () => {
        render(MacroConstraint, {
            label: 'Protein',
            minValue: '',
            maxValue: 100
        });

        const inputs = screen.getAllByRole('spinbutton');
        const minInput = inputs[0];

        await fireEvent.input(minInput, { target: { value: 'abc' } });
        await fireEvent.blur(minInput);

        expect(minInput.value).toBe('');
    });
});
