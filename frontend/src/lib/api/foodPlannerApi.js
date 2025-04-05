import ky from "ky";
import {CONFIG} from "$lib/config/config.js";


const api = ky.create({
    prefixUrl: CONFIG.API.URL,
    headers: {
        "Content-Type": "application/json",
    },
    timeout: 10000,
    retry: 2
});

export const getDates = async () => {
    try {
        return await api.get(CONFIG.API.ENDPOINT.DATES).json();
    } catch (error) {
        console.error("❌ Failed to fetch dates:", error.message);
        throw error;
    }
};

export const getMealPlan = async (mealPlanRequestParams) => {
    try {
        return await api.post(CONFIG.API.ENDPOINT.MEAL_PLAN, {json: mealPlanRequestParams}).json();
    } catch (error) {
        console.error("❌ Failed to fetch meal plan:", error.message);
        throw error;
    }
};

