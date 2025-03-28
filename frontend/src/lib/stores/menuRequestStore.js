import {writable} from 'svelte/store';

function createMenuRequestStore() {
    const {subscribe, set, update} = writable({
        macroConstraints: [
            {name: "Calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true},
            {name: "Protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true},
            {name: "Carb", min: undefined, max: undefined, unit: "g", emoji: "🥖", isValid: true},
            {name: "Fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true}
        ],
        selectedDate: null,
        dislikedFoods: [],
        maxFoodRepeat: null,
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
        }
    };
}

export const menuRequestStore = createMenuRequestStore();
