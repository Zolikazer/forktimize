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
        foodVendor: null,
        status: MealPlanStatus.NOT_STARTED,
    });

    return {
        subscribe,

        setLoading: () => update(s => ({...s, status: MealPlanStatus.IN_PROGRESS})),
        setSuccess: (foods, logEntry, date, totalPrice, totalCalories, totalProtein, totalCarbs, totalFat, foodVendor) => set({
            foods: foods,
            foodLogEntry: logEntry,
            date: date,
            totalPrice: totalPrice,
            totalCalories: totalCalories,
            totalProtein: totalProtein,
            totalCarbs: totalCarbs,
            totalFat: totalFat,
            foodVendor: foodVendor,
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
            foodVendor: null,
            status: MealPlanStatus.NOT_STARTED
        }),
        removeFood: (foodName) =>
            update(state => {
                const foodsToRemove = state.foods.filter(food => food.name === foodName);

                const totalToSubtract = foodsToRemove.reduce(
                    (acc, food) => ({
                        price: acc.price + food.price,
                        calories: acc.calories + food.calories,
                        protein: acc.protein + food.protein,
                        carbs: acc.carbs + food.carb,
                        fat: acc.fat + food.fat,
                    }),
                    { price: 0, calories: 0, protein: 0, carbs: 0, fat: 0 }
                );


                return {
                    ...state,
                    totalPrice: state.totalPrice - totalToSubtract.price,
                    totalCalories: state.totalCalories - totalToSubtract.calories,
                    totalProtein: state.totalProtein - totalToSubtract.protein,
                    totalCarbs: state.totalCarbs - totalToSubtract.carbs,
                    totalFat: state.totalFat - totalToSubtract.fat,
                    foods: state.foods.filter(food => food.name !== foodName),
                };
            })
    };
}

export const mealPlanStore = createMealPlanStore();

