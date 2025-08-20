import {fireEvent, render, screen, waitFor} from '@testing-library/svelte';
import MealPlan from '$lib/components/meal-plan/MealPlan.svelte';
import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
import {vendorListStore} from "$lib/stores/foodVendorStore.js";
import {beforeEach, describe, expect, test, vi} from 'vitest';

// Mock the postMessage API
const mockPostMessage = vi.fn();
const mockAddEventListener = vi.fn();

beforeEach(() => {
    // Reset stores
    mealPlanStore.reset();
    vendorListStore.set([
        { type: 'cityfood', name: 'CityFood', menuUrl: 'https://cityfood.hu' },
        { type: 'efood', name: 'eFood', menuUrl: 'https://efood.hu' }
    ]);

    // Reset mocks
    mockPostMessage.mockClear();
    mockAddEventListener.mockClear();

    // Mock window.postMessage and addEventListener
    Object.defineProperty(window, 'postMessage', {
        value: mockPostMessage,
        writable: true
    });
    Object.defineProperty(window, 'addEventListener', {
        value: mockAddEventListener,
        writable: true
    });
});

describe('MealPlan component', () => {
    const mockFoods = [
        {
            id: 1,
            name: "Test Food 1",
            calories: 300,
            protein: 20,
            carb: 40,
            fat: 10,
            price: 1500
        },
        {
            id: 2,
            name: "Test Food 2",
            calories: 250,
            protein: 15,
            carb: 30,
            fat: 8,
            price: 1200
        }
    ];

    test('renders meal plan with foods correctly', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        expect(screen.getByText('Your Meal Plan')).toBeInTheDocument();
        expect(screen.getByText('2 items')).toBeInTheDocument();
        expect(screen.getByText('Test Food 1')).toBeInTheDocument();
        expect(screen.getByText('Test Food 2')).toBeInTheDocument();
    });

    test('sends handshake SYN message with vendor information on mount', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        expect(mockPostMessage).toHaveBeenCalledWith({
            type: 'FORKTIMIZE_HANDSHAKE_SYN',
            vendor: 'cityfood'
        }, '*');
    });

    test('registers message event listener on mount', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        expect(mockAddEventListener).toHaveBeenCalledWith('message', expect.any(Function));
    });

    test('does not show extension button when extension is not present', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        expect(screen.queryByText('📱 Send to Extension')).not.toBeInTheDocument();
    });

    test('shows enabled extension button when vendor is supported', async () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        // Simulate extension response with vendor support
        const messageHandler = mockAddEventListener.mock.calls[0][1];
        messageHandler({
            data: {
                type: 'FORKTIMIZE_HANDSHAKE_ACK',
                vendorSupported: true
            }
        });

        await waitFor(() => {
            const button = screen.getByText('📱 Send to Extension');
            expect(button).toBeInTheDocument();
            expect(button).not.toBeDisabled();
            expect(button).toHaveClass('is-success');
            expect(button).not.toHaveClass('is-warning');
        });
    });

    test('shows disabled extension button when vendor is not supported', async () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'unsupported-vendor'
        );

        render(MealPlan);

        // Simulate extension response without vendor support
        const messageHandler = mockAddEventListener.mock.calls[0][1];
        messageHandler({
            data: {
                type: 'FORKTIMIZE_HANDSHAKE_ACK',
                vendorSupported: false
            }
        });

        await waitFor(() => {
            const button = screen.getByText('📱 Send to Extension');
            expect(button).toBeInTheDocument();
            expect(button).toBeDisabled();
            expect(button).toHaveClass('is-warning');
            expect(button).not.toHaveClass('is-success');
            expect(button).toHaveAttribute('title', "Extension doesn't support this vendor yet");
        });
    });

    test('sends meal plan data when enabled button is clicked', async () => {
        const testDate = '2025-01-15';
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            testDate,
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        // Simulate extension response with vendor support
        const messageHandler = mockAddEventListener.mock.calls[0][1];
        messageHandler({
            data: {
                type: 'FORKTIMIZE_HANDSHAKE_ACK',
                vendorSupported: true
            }
        });

        await waitFor(() => {
            expect(screen.getByText('📱 Send to Extension')).toBeInTheDocument();
        });

        const button = screen.getByText('📱 Send to Extension');
        await fireEvent.click(button);

        expect(mockPostMessage).toHaveBeenCalledWith({
            type: 'FORKTIMIZE_MEAL_PLAN_DATA',
            data: {
                date: testDate,
                foodVendor: 'cityfood',
                foods: mockFoods,
                exportedAt: expect.any(String)
            }
        }, '*');
    });

    test('disabled button does not send data when clicked', async () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'unsupported-vendor'
        );

        render(MealPlan);

        // Simulate extension response without vendor support
        const messageHandler = mockAddEventListener.mock.calls[0][1];
        messageHandler({
            data: {
                type: 'FORKTIMIZE_HANDSHAKE_ACK',
                vendorSupported: false
            }
        });

        await waitFor(() => {
            expect(screen.getByText('📱 Send to Extension')).toBeDisabled();
        });

        // Reset call count to only track clicks after handshake
        mockPostMessage.mockClear();

        const button = screen.getByText('📱 Send to Extension');
        await fireEvent.click(button);

        // Should not send meal plan data since button is disabled
        expect(mockPostMessage).not.toHaveBeenCalledWith(
            expect.objectContaining({
                type: 'FORKTIMIZE_MEAL_PLAN_DATA'
            }),
            '*'
        );
    });

    test('displays correct vendor name and link in subtitle', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        const vendorLink = screen.getByText('CityFood');
        expect(vendorLink).toBeInTheDocument();
        expect(vendorLink).toHaveAttribute('href', 'https://cityfood.hu');
        expect(vendorLink).toHaveAttribute('target', '_blank');
    });

    test('handles unknown vendor gracefully', () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'unknown-vendor'
        );

        render(MealPlan);

        expect(screen.getByText('Forktimize')).toBeInTheDocument();
    });

    test('ignores non-ACK messages', async () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        const messageHandler = mockAddEventListener.mock.calls[0][1];
        
        // Send a different message type
        messageHandler({
            data: {
                type: 'SOME_OTHER_MESSAGE',
                vendorSupported: true
            }
        });

        // Extension button should not appear since ACK was not received
        expect(screen.queryByText('📱 Send to Extension')).not.toBeInTheDocument();
    });

    test('handles ACK message without vendorSupported property', async () => {
        mealPlanStore.setSuccess(
            mockFoods,
            null,
            '2025-01-15',
            2700,
            550,
            35,
            70,
            18,
            'cityfood'
        );

        render(MealPlan);

        const messageHandler = mockAddEventListener.mock.calls[0][1];
        messageHandler({
            data: {
                type: 'FORKTIMIZE_HANDSHAKE_ACK'
                // vendorSupported property missing
            }
        });

        await waitFor(() => {
            const button = screen.getByText('📱 Send to Extension');
            expect(button).toBeInTheDocument();
            expect(button).toBeDisabled();
            expect(button).toHaveClass('is-warning');
        });
    });
});