export class FoodPlannerClient {
    static async getDates() {
        // fetch data from server
        const res = await fetch("https://example.com/dates");
        if (res.ok) {
            return await res.json();
        } else {
            console.log("Failed to fetch dates");
            return [];
        }
    }

    static async getMenuPlan(constraints) {
        const res = await fetch("https://example.com/menu", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(constraints),
        });
        if (res.ok) {
            let response = await res.json();
            console.log(response);
            return {statusCode: res.status, data: response};
        } else {
            console.log("Failed to fetch menu");
            return {foods: []};
        }
    }
}
