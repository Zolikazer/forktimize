import { writable } from "svelte/store";

// ✅ Store to track error messages and visibility
export const errorStore = writable({
    show: false,
    message: ""
});

// ✅ Function to show an error
export function showError(message) {
    errorStore.set({ show: true, message });
}

// ✅ Function to hide the error
export function hideError() {
    errorStore.set({ show: false, message: "" });
}
