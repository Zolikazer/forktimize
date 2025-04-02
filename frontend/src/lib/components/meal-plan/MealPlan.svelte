<script>
    import FoodCard from "$lib/components/meal-plan/FoodCard.svelte";
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import {getProviderLabel} from "$lib/utils/foodProviders.js";
</script>

<div class="card">
    <SectionHeader title="Your Meal Plan" subTitle={`🛵 Order these from ${getProviderLabel($mealPlanStore.foodProvider)}`}>
            <span slot="tags" class="tag is-light is-success bigger-tag">
      🍱 {$mealPlanStore.foods.length} items
    </span>
    </SectionHeader>
    <div class="is-flex is-flex-wrap-wrap mt-5 p-3">
        {#each $mealPlanStore.foods as food}
            <FoodCard food={food}/>
        {/each}
    </div>
</div>
