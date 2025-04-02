import {writable} from "svelte/store";

export const MealPlanStatus = {
    NOT_STARTED: "notGenerated",
    IN_PROGRESS: "inProgress",
    SUCCESS: "success",
    FAILURE: "failure"
};

function createMealPlanStore() {
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
        status: MealPlanStatus.NOT_STARTED,
    });

    return {
        subscribe,

        setLoading: () => update(s => ({...s, status: MealPlanStatus.IN_PROGRESS})),
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
            status: MealPlanStatus.SUCCESS
        }),
        setFailure: () => update(s => ({...s, foods: null, status: MealPlanStatus.FAILURE})),
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
            status: MealPlanStatus.NOT_STARTED
        }),
        removeFood: (foodName) =>
            update(state => ({
                ...state,
                foods: state.foods.filter(food => food.name !== foodName)
            }))
    };
}

export const mealPlanStore = createMealPlanStore();

