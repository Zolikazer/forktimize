// src/stores/foodStore.js
import { writable } from "svelte/store";

export const menu = writable(null);

export const MenuStatusEnum = {
    NOT_GENERATED: "notGenerated",
    IN_PROGRESS: "inProgress",
    SUCCESS: "success",
    FAILURE: "failure"
};

export const currentMenuStatus = writable(MenuStatusEnum.NOT_GENERATED);
