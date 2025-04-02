import {writable} from 'svelte/store';
import {FoodProvider} from "$lib/utils/foodProviders.js";

function createMealPlanRequestStore() {
    const {subscribe, set, update} = writable({
        selectedDate: null,
        foodProvider: FoodProvider.CITY_FOOD.value,
        dislikedFoods: [],
        maxFoodRepeat: null,
        macroConstraints: [
            {name: "Calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true},
            {name: "Protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true},
            {name: "Carb", min: undefined, max: undefined, unit: "g", emoji: "🥖", isValid: true},
            {name: "Fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true}
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
                {name: "Calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true},
                {name: "Protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true},
                {name: "Carb", min: undefined, max: undefined, unit: "g", emoji: "🥖", isValid: true},
                {name: "Fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true}
            ],
            selectedDate: null,
            dislikedFoods: [],
            maxFoodRepeat: null,
            foodProvider: FoodProvider.CITY_FOOD.value,
        })
    };
}

export const mealPlanRequestStore = createMealPlanRequestStore();
