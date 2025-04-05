<script>
    import MacroConstraint from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";
    import {MealPlanStatus, mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import {getMealPlan} from "$lib/api/foodPlannerApi.js";
    import {showError} from "$lib/stores/errorStore.js";
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
    import {get} from "svelte/store";
    import MaxFoodRepeat from "$lib/components/forms/MaxFoodRepeat.svelte";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import FoodVendorSelector from "$lib/components/forms/FoodVendorSelector.svelte";


    async function generateMealPlan() {
        mealPlanStore.setLoading();
        const formState = get(mealPlanRequestStore);
        const mealPlanRequest = createMealPlanRequest(formState);

        try {
            const mealPlan = await getMealPlan(mealPlanRequest)
            if (mealPlan.foods.length > 0) {
                mealPlanStore.setSuccess(
                    mealPlan.foods,
                    mealPlan.foodLogEntry,
                    mealPlan.date,
                    mealPlan.totalPrice,
                    mealPlan.totalCalories,
                    mealPlan.totalProtein,
                    mealPlan.totalCarbs,
                    mealPlan.totalFat,
                    mealPlan.foodVendor
                )
            } else {
                mealPlanStore.setFailure()
            }
        } catch (error) {
            mealPlanStore.setFailure()
            showError(error.message);
        }
    }

    export function createMealPlanRequest(formState) {
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
            foodVendor: formState.foodVendor,
        };
    }

    $: formData = $mealPlanRequestStore;
    $: allConstraintsValid = $mealPlanRequestStore.macroConstraints.every(
        ({min, max}) => min == null || max == null || min < max
    );


</script>

<div class="card">
    <SectionHeader title="Set Your Nutritional Goals" subTitle="Give us the requirements, we give you the plan!">
        <div class="tags" slot="tags">
            <FoodVendorSelector/>
        </div>
    </SectionHeader>
    <div class="card-content">
        <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2 mt-3">
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
                <MaxFoodRepeat bind:maxFoodRepeat={$mealPlanRequestStore.maxFoodRepeat}/>
            </div>
        </div>


        <div class="has-text-centered">
            <button class="button generate-button is-fullwidth has-text-weight-bold is-rounded is-medium p-3 is-size-5 "
                    on:click={generateMealPlan}
                    disabled={$mealPlanStore.status === MealPlanStatus.IN_PROGRESS || !allConstraintsValid}>Generate
                Meal Plan 🍽️
            </button>
        </div>
    </div>
</div>
<style>
    .generate-button {
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
