import {writable} from 'svelte/store';
import {FoodVendor} from "$lib/utils/foodVendors.js";

function createMealPlanRequestStore() {
    const {subscribe, set, update} = writable({
        selectedDate: null,
        foodVendor: FoodVendor.CITY_FOOD.value,
        dislikedFoods: [],
        maxFoodRepeat: null,
        macroConstraints: [
            {name: "calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true},
            {name: "protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true},
            {name: "carb", min: undefined, max: undefined, unit: "g", emoji: "🍞", isValid: true},
            {name: "fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true}
        ],
    });

    return {
        subscribe,
        set,
        update,
        addDislikedFood: (food) => {
            update(state => {
                if (!state.dislikedFoods.includes(food)) {
                    return {
                        ...state,
                        dislikedFoods: [...state.dislikedFoods, food]
                    };
                }
                return state;
            });
        },
        removeDislikedFood: (food) => {
            update(state => ({
                ...state,
                dislikedFoods: state.dislikedFoods.filter(f => f !== food)
            }));
        },
        setSelectedDate: (date) => {
            update(state => ({
                ...state,
                selectedDate: date
            }));
        },
        reset: () => set({
            macroConstraints: [
                {name: "calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true},
                {name: "protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true},
                {name: "carb", min: undefined, max: undefined, unit: "g", emoji: "🥖", isValid: true},
                {name: "fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true}
            ],
            selectedDate: null,
            dislikedFoods: [],
            maxFoodRepeat: null,
            foodVendor: FoodVendor.CITY_FOOD.value,
        })
    };
}

export const mealPlanRequestStore = createMealPlanRequestStore();
