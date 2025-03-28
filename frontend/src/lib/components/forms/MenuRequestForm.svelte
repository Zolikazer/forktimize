<script>
    import MacroConstraint from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";
    import {MenuGenerationStatus, menuStore} from "$lib/stores/menuStore.js";
    import {getMenuPlan} from "$lib/api/foodPlannerClient.js";
    import {showError} from "$lib/stores/errorStore.js";
    import {menuRequestStore} from "$lib/stores/menuRequestStore.js";
    import {get} from "svelte/store";
    import MaxFoodRepeat from "$lib/components/forms/MaxFoodRepeat.svelte";


    async function generateMenu() {
        menuStore.setLoading();
        const formState = get(menuRequestStore);
        const menuRequest = createMenuRequest(formState);

        try {
            const generatedMenu = await getMenuPlan(menuRequest)
            if (generatedMenu.foods.length > 0) {
                menuStore.setSuccess(
                    generatedMenu.foods,
                    generatedMenu.foodLogEntry,
                    generatedMenu.date,
                    generatedMenu.totalPrice,
                    generatedMenu.totalCalories,
                    generatedMenu.totalProtein,
                    generatedMenu.totalCarbs,
                    generatedMenu.totalFat
                )
            } else {
                menuStore.setFailure()
            }
        } catch (error) {
            menuStore.setFailure()
            showError(error.message);
        }
    }

    export function createMenuRequest(formState) {
        const nutritionalConstraints = formState.macroConstraints.reduce((acc, constraint) => {
            acc[`min${constraint.name}`] = constraint.min;
            acc[`max${constraint.name}`] = constraint.max;
            return acc;
        }, {});

        return {
            nutritionalConstraints,
            date: formState.selectedDate,
            foodBlacklist: formState.dislikedFoods,
            maxFoodRepeat: formState.maxFoodRepeat,
        };
    }

    $: formData = $menuRequestStore;
    $: allConstraintsValid = $menuRequestStore.macroConstraints.every(
        ({ min, max }) => min == null || max == null || min < max
    );


</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Set Your Nutritional Goals</h2>

    <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2">
        {#each formData.macroConstraints as constraint, index (constraint.name)}
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
            <DateSelector/>
        </div>
        <div class="column">
            <FoodBlacklist/>
        </div>
        <div class="column is-narrow">
            <MaxFoodRepeat bind:maxFoodRepeat={$menuRequestStore.maxFoodRepeat} />
        </div>
    </div>


    <div class="has-text-centered">
        <button class="button generate-button is-fullwidth has-text-weight-bold is-rounded is-medium p-3 is-size-5 "
                on:click={generateMenu}
                disabled={$menuStore.status === MenuGenerationStatus.IN_PROGRESS || !allConstraintsValid}>Generate My Menu 🍽️
        </button>
    </div>
</div>

<style>
    .generate-button {
        font-size: 1rem;
        background: #00d1b2;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.03);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }
</style>
