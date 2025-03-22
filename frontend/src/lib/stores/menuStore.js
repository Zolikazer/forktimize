// src/stores/foodStore.js
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
        status: MenuGenerationStatus.NOT_STARTED
    });

    return {
        subscribe,

        setLoading: () => update(s => ({...s, status: MenuGenerationStatus.IN_PROGRESS})),
        setSuccess: (foods, logEntry) => set({
            foods: foods,
            foodLogEntry: logEntry,
            status: MenuGenerationStatus.SUCCESS
        }),
        setFailure: () => update(s => ({...s, foods: null, status: MenuGenerationStatus.FAILURE})),
        reset: () => set({
            data: null,
            foodLogEntry: null,
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


export const menu = writable(null);
export const foodLogEntryStore = writable(null)

export const menuStatus = writable(MenuGenerationStatus.NOT_STARTED);

