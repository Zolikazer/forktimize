// src/stores/foodStore.js
import { writable } from "svelte/store";

export const menu = writable(null);
export const foodLogEntryStore = writable(null)

export const MenuGenerationStatus = {
    NOT_GENERATED: "notGenerated",
    IN_PROGRESS: "inProgress",
    SUCCESS: "success",
    FAILURE: "failure"
};

export const menuStatus = writable(MenuGenerationStatus.NOT_GENERATED);
