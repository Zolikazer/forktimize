import {render, screen} from '@testing-library/svelte';
import {describe, expect, test} from 'vitest';
import MacroStat from "$lib/components/plan-summary/MacroStat.svelte";


describe('MacroStat Component', () => {

    test('renders correctly with given props', () => {
        render(MacroStat, {
            icon: '💪',
            label: 'Protein',
            value: '100g',
            subValue: '30%',
            colorClass: 'danger'
        });

        expect(screen.getByText('Protein')).toBeInTheDocument();
        expect(screen.getByText('100g')).toBeInTheDocument();
        expect(screen.getByText('30%')).toBeInTheDocument();
    });

});
