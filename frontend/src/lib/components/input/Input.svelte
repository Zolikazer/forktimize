<script>
    import MacroConstraint from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";
    import {menu} from "$lib/stores/menuStore.js";
    import {FoodPlannerClient} from "$lib/foodPlannerClient.js";
    import {showError} from "$lib/stores/errorStore.js";
    import {dislikedFoods} from "$lib/stores/dislikedFoodsStore.js";


    let calorieConstraint = {
        min: 2300,
        max: 2700,
        isValid: true
    }

    let proteinConstraint = {
        min: undefined,
        max: undefined,
        isValid: true
    }

    let carbConstraint = {
        min: undefined,
        max: undefined,
        isValid: true
    }

    let fatConstraint = {
        min: undefined,
        max: undefined,
        isValid: true
    }


    export let dates = [];
    let date = dates[0];

    function generateMenu() {
        console.log(calorieConstraint.max)
        try {
            FoodPlannerClient.getMenuPlan(createRequestBody())
                .then(response => {
                    menu.set(response.data.foods);
                })
                .catch(error => {
                    showError(`${error.message}`);
                });
        } catch (error) {
            console.log("aAAAAAAAAAAAAAAAA")
        }
    }

    function createRequestBody() {
        return {
            nutritionalConstraints: {
                minCalories: calorieConstraint.min,
                maxCalories: calorieConstraint.max,
                minProtein: proteinConstraint.min,
                maxProtein: proteinConstraint.max,
                minCarb: carbConstraint.min,
                maxCarb: carbConstraint.max,
                minFat: fatConstraint.min,
                maxFat: fatConstraint.max,
            },
            date,
            foodBlacklist: $dislikedFoods,
        };
    }

</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Set Your Nutritional Goals</h2>

    <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2">
        <MacroConstraint label="Calories" bind:minValue={calorieConstraint.min}
                         bind:maxValue={calorieConstraint.max}
                         bind:isValid={calorieConstraint.isValid}
                         unit="kcal"
                         emoji="🔥"/>
        <MacroConstraint label="Protein" bind:minValue={proteinConstraint.min}
                         bind:maxValue={proteinConstraint.max}
                         bind:isValid={proteinConstraint.isValid}
                         unit="g" emoji="💪"/>
        <MacroConstraint label="Carbs" bind:minValue={carbConstraint.min}
                         bind:maxValue={carbConstraint.max}
                         bind:isValid={carbConstraint.isValid}
                         unit="g"
                         emoji="🥖"/>
        <MacroConstraint label="Fats" bind:minValue={fatConstraint.min}
                         bind:maxValue={fatConstraint.max}
                         bind:isValid={fatConstraint.isValid}
                         unit="g"
                         emoji="🧈"/>
    </div>

    <div class="columns is-centered mt-3">
        <div class="column">
            <DateSelector dates={dates} bind:minValue={date}/>
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
