import { writable } from "svelte/store";

export const errorStore = writable({
    show: false,
    message: ""
});

export function showError(message) {
    errorStore.set({ show: true, message });
}

export function hideError() {
    errorStore.set({ show: false, message: "" });
}
