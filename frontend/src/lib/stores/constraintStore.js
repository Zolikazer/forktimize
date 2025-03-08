import { writable } from "svelte/store";

export const macroConstraints = writable([
    { name: "Calories", min: 2300, max: 2700, unit: "kcal", emoji: "🔥", isValid: true },
    { name: "Protein", min: undefined, max: undefined, unit: "g", emoji: "💪", isValid: true },
    { name: "Carb", min: undefined, max: undefined, unit: "g", emoji: "🥖", isValid: true },
    { name: "Fat", min: undefined, max: undefined, unit: "g", emoji: "🧈", isValid: true }
]);
