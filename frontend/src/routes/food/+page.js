// src/routes/dates/+page.server.js

import {FoodPlannerClient} from "$lib/foodPlannerClient.js";

export async function load() {
    if (import.meta.env.MODE === "development") {
        return {dates: ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]};
    }

    return {dates: await FoodPlannerClient.getDates()};
}
