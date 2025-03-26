import {render, screen} from '@testing-library/svelte';
import {describe, expect, test} from "vitest";
import SectionHeader from "$lib/components/common/SectionHeader.svelte";

describe('Header Component', () => {

    test('renders title and subtitle correctly', () => {
        render(SectionHeader, {title: 'Test Title', subTitle: 'Test Subtitle'});

        expect(screen.getByText('Test Title')).toBeInTheDocument();
        expect(screen.getByText('Test Subtitle')).toBeInTheDocument();
    });


    test('does not break if subtitle is empty', () => {
        render(SectionHeader, {title: 'Only Title'});

        expect(screen.getByText('Only Title')).toBeInTheDocument();
        expect(screen.queryByRole('subtitle')).not.toBeInTheDocument();
    });
});
