import {writable} from "svelte/store";

export const MenuGenerationStatus = {
    NOT_STARTED: "notGenerated",
    IN_PROGRESS: "inProgress",
    SUCCESS: "success",
    FAILURE: "failure"
};

function createMenuStore() {
    const {subscribe, set, update} = writable({
        foods: null,
        foodLogEntry: null,
        date: null,
        totalPrice: null,
        totalCalories: null,
        totalProtein: null,
        totalCarbs: null,
        totalFat: null,
        foodProvider: null,
        status: MenuGenerationStatus.NOT_STARTED,
    });

    return {
        subscribe,

        setLoading: () => update(s => ({...s, status: MenuGenerationStatus.IN_PROGRESS})),
        setSuccess: (foods, logEntry, date, totalPrice, totalCalories, totalProtein, totalCarbs, totalFat, foodProvider) => set({
            foods: foods,
            foodLogEntry: logEntry,
            date: date,
            totalPrice: totalPrice,
            totalCalories: totalCalories,
            totalProtein: totalProtein,
            totalCarbs: totalCarbs,
            totalFat: totalFat,
            foodProvider: foodProvider,
            status: MenuGenerationStatus.SUCCESS
        }),
        setFailure: () => update(s => ({...s, foods: null, status: MenuGenerationStatus.FAILURE})),
        reset: () => set({
            foods: null,
            foodLogEntry: null,
            date: null,
            totalPrice: null,
            totalCalories: null,
            totalProtein: null,
            totalCarbs: null,
            totalFat: null,
            foodProvider: null,
            status: MenuGenerationStatus.NOT_STARTED
        }),
        removeFood: (foodName) =>
            update(state => ({
                ...state,
                foods: state.foods.filter(food => food.name !== foodName)
            }))
    };
}

export const menuStore = createMenuStore();

