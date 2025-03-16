import {SETTINGS} from "../settings.js";

export class FoodPlannerClient {
    static async getDates() {
        // fetch data from server
        const res = await fetch(`${SETTINGS.API.URL}/${SETTINGS.API.ENDPOINT.DATES}`);

        if (res.ok) {
            const foo = await res.json()
            console.log("Successfully fetched dates.");
            return foo;
        } else {
            console.log("Failed to fetch dates.");
            return [];
        }
    }

    static async getMenuPlan(constraints) {
        const res = await fetch(`${SETTINGS.API.URL}/${SETTINGS.API.ENDPOINT.MENU}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'Cache-Control': 'no-cache'
            },
            cache: 'no-store',
            body: JSON.stringify(constraints),
        });
        if (res.ok) {
            let response = await res.json();
            console.log(response);
            return {statusCode: res.status, data: response};
        } else {
            console.log(res.status)
            throw new Error("Failed to fetch menu.");
        }
    }
}
