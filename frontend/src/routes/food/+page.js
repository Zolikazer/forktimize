import {FoodPlannerClient} from "$lib/foodPlannerClient.js";

export async function load() {
    if (import.meta.env.MODE === "development" && import.meta.env.VITE_RUN_MOCK_BACKEND === "true") {

        return {dates: ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]};
    }

    return {dates: await FoodPlannerClient.getDates()};
}
