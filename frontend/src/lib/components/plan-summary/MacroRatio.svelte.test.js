import { render, screen } from '@testing-library/svelte';
import {describe, expect, test} from 'vitest';
import MacroRatio from "$lib/components/plan-summary/MacroRatio.svelte";

describe('MacroRatio Component', () => {

    test('renders correctly with given percentages', () => {
        render(MacroRatio, {
            proteinPercentage: 50,
            carbsPercentage: 35,
            fatPercentage: 15,
            title: 'Test Macronutrient Ratio'
        });

        expect(screen.getByText(/Macronutrient Ratio/i)).toBeInTheDocument();
        expect(screen.getByText(/35%/i)).toBeInTheDocument();
        expect(screen.getByText(/50%/i)).toBeInTheDocument();
        expect(screen.getByText(/15%/i)).toBeInTheDocument();

        expect(screen.getByText(/Protein/i)).toBeInTheDocument();
        expect(screen.getByText(/Carbs/i)).toBeInTheDocument();
        expect(screen.getByText(/Fat/i)).toBeInTheDocument();
    });

    test('does not display percentage text if percentage is 10% or lower', () => {
        render(MacroRatio, {
            proteinPercentage: 10,
            carbsPercentage: 9,
            fatPercentage: 5
        });

        expect(screen.queryByText('10%')).not.toBeInTheDocument();
        expect(screen.queryByText('9%')).not.toBeInTheDocument();
        expect(screen.queryByText('5%')).not.toBeInTheDocument();
    });

    test('renders correct segment widths based on percentages', () => {
        const { container } = render(MacroRatio, {
            proteinPercentage: 50,
            carbsPercentage: 30,
            fatPercentage: 20
        });

        const segments = container.querySelectorAll('.ratio-segment');
        expect(segments[0]).toHaveStyle('width: 50%');
        expect(segments[1]).toHaveStyle('width: 30%');
        expect(segments[2]).toHaveStyle('width: 20%');
    });
});
