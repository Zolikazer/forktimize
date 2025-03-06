class FoodPlannerClient {
    getFoodPlan() {
        // fetch data from server
        return fetch('/foodPlan').then(response => response.json());
    }
}
