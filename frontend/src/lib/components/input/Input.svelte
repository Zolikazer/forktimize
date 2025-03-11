<script>
    import MacroConstraint from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";
    import {menu} from "$lib/stores/menuStore.js";
    import {FoodPlannerClient} from "$lib/foodPlannerClient.js";
    import {showError} from "$lib/stores/errorStore.js";
    import {dislikedFoods} from "$lib/stores/dislikedFoodsStore.js";
    import {macroConstraints} from "$lib/stores/constraintStore.js";
    import {get} from "svelte/store";


    export let dates = [];
    let selectedDate = dates.length ? dates[0] : "";

    async function generateMenu() {
        try {
            console.log(get(macroConstraints));
            console.log(get(dislikedFoods));
            const requestBody = createMenuRequest(get(macroConstraints), selectedDate, get(dislikedFoods));
            const response = await FoodPlannerClient.getMenuPlan(requestBody);
            menu.set(response.data.foods);
        } catch (error) {
            showError(error.message);
            console.error("Menu generation failed:", error);
        }
    }
    export function createMenuRequest(macroConstraints, selectedDate, dislikedFoods) {
        if (!selectedDate) throw new Error("No date selected for menu generation.");

        const nutritionalConstraints = macroConstraints.reduce((acc, constraint) => {
            acc[`min${constraint.name}`] = constraint.min;
            acc[`max${constraint.name}`] = constraint.max;
            return acc;
        }, {});

        return {
            nutritionalConstraints,
            date: selectedDate,
            foodBlacklist: dislikedFoods,
        };
    }


</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Set Your Nutritional Goals</h2>

    <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2">
        {#each $macroConstraints as constraint (constraint.name)}
            <MacroConstraint
                    bind:minValue={constraint.min}
                    bind:maxValue={constraint.max}
                    bind:isValid={constraint.isValid}
                    label={constraint.name}
                    unit={constraint.unit}
                    emoji={constraint.emoji}
            />
        {/each}
    </div>

    <div class="columns is-centered mt-3">
        <div class="column">
            <DateSelector dates={dates} bind:selectedDate={selectedDate}/>
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
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.03);
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.3);
    }
</style>
