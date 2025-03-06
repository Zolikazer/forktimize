// src/routes/dates/+page.server.js

import {FoodPlannerClient} from "$lib/foodPlannerClient.js";

export async function load() {
    return {dates: await FoodPlannerClient.getDates()};
}
