import {render, screen} from '@testing-library/svelte';
import MacroStat from "$lib/components/menu/summary/MacroStat.svelte";
import {describe, expect, test} from 'vitest';


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
        expect(screen.getByText('💪')).toBeInTheDocument();
    });

});
