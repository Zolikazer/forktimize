// src/stores/foodStore.js
import { writable } from "svelte/store";

export const menu = writable(null);

export const MenuStatusEnum = {
    NOT_GENERATED: "notGenerated",
    IN_PROGRESS: "inProgress",  // ✅ New state added
    SUCCESS: "success",
    FAILURE: "failure"
};

// 🔥 New store to track menu generation status
export const currentMenuStatus = writable(MenuStatusEnum.NOT_GENERATED);
