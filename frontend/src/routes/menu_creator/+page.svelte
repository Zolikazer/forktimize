<script>
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import {fade} from 'svelte/transition';
    import MenuRequestForm from "$lib/components/forms/MenuRequestForm.svelte";
    import Help from "$lib/components/feedback/Help.svelte";
    import MealPlan from "$lib/components/meal-plan/MealPlan.svelte";
    import MenuSummary from "$lib/components/plan-summary/MenuSummary.svelte";
    import FoodLogEntry from "$lib/components/food-log/FoodLogEntry.svelte";

    export let data = {dates: []};

</script>

<section class="mt-5">
    <div class="container is-fluid">
        <div class="columns is-centered">
            <div class="column">
                <MenuRequestForm dates={data.dates}/>
            </div>
            <div class="column">
                <Help/>
            </div>
        </div>

        {#if $mealPlanStore.foods && $mealPlanStore.foods.length > 0}
            <div class="columns is-centered" transition:fade={{ duration: 150 }}>
                <div class="column">
                    <MealPlan/>
                </div>
                <div class="column">
                    <MenuSummary/>
                    <FoodLogEntry/>
                </div>
            </div>
        {/if}
    </div>
</section>
