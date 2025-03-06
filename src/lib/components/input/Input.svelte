<script>
    import MacroConstraint from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";
    import {menu} from "$lib/stores/menuStore.js";
    import {FoodPlannerClient} from "$lib/foodPlannerClient.js";


    let minCalories = 2000;
    let maxCalories = 2500;
    let minProtein;
    let maxProtein;
    let minCarbs;
    let maxCarbs;
    let minFats;
    let maxFats;


    export let dates = [];
    let selectedDate = dates[0];

    function createRequestBody() {
        const requestBody = {
            minCalories,
            maxCalories,
            minProtein,
            maxProtein,
            minCarbs,
            maxCarbs,
            minFats,
            maxFats
        };

        // ✅ Remove undefined values and convert keys to snake_case
        return Object.fromEntries(
            Object.entries(requestBody)
                .filter(([_, value]) => value !== undefined) // Remove undefined values
                .map(([key, value]) => [toSnakeCase(key), value]) // Convert keys to snake_case
        );
    }

    function toSnakeCase(str) {
        return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
    }

    let aFood = {
        name: "Brünni sertésborda (mustárban pácolt) rántva, rizi-bizi buziiiiiiiiiiiiiiiiiiiiiiiiiiiii",
        calories: 300,
        protein: 400,
        carbs: 100,
        fats: 78,
        price: 2565
    };

    function generateMenu() {
        FoodPlannerClient.getMenuPlan(createRequestBody())
            .then(response => {
                menu.set(response.foods);
            })
            .catch(error => {
                console.error(error);
            });
    }

    // function generateMenu() {
    //     menu.set([
    //         aFood,
    //         {name: "Quinoa Salad", calories: 250, protein: 8, carbs: 45, fats: 4, price: 1600},
    //         {name: "Rántott fasza hús", calories: 450, protein: 8, carbs: 36, fats: 38, price: 2000},
    //         {name: "Quinoa Salad", calories: 250, protein: 8, carbs: 45, fats: 4, price: 3560},
    //         {name: "Saláta", calories: 250, protein: 8, carbs: 45, fats: 4, price: 3560},
    //         aFood
    //     ]);
    // }


</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Set Your Nutritional Goals</h2>

    <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2">
        <MacroConstraint label="Calories" bind:minValue={minCalories} bind:maxValue={maxCalories} unit="kcal"
                         emoji="🔥"/>
        <MacroConstraint label="Protein" bind:minValue={minProtein} bind:maxValue={maxProtein} unit="g" emoji="💪"/>
        <MacroConstraint label="Carbs" bind:minValue={minCarbs} bind:maxValue={maxCarbs} unit="g" emoji="🥖"/>
        <MacroConstraint label="Fats" bind:minValue={minFats} bind:maxValue={maxFats} unit="g" emoji="🧈"/>
    </div>

    <div class="columns is-centered mt-3">
        <div class="column">
            <DateSelector dates={dates} bind:minValue={selectedDate}/>
        </div>
        <div class="column">
            <FoodBlacklist/>
        </div>
    </div>


    <div class="has-text-centered">
        <button class="button generate-button is-fullwidth has-text-weight-bold is-rounded is-medium p-3  is-size-5 "
                on:click={generateMenu}>Generate My Menu 🍽️
        </button>
    </div>
</div>

<style>
    .generate-button {
        font-size: 1rem;
        background: #00d1b2;
        /*color: white;*/
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.03);
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.3);
    }
</style>
