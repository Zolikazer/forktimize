<script>
    import FoodCard from "$lib/components/meal-plan/FoodCard.svelte";
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import {t} from "$lib/stores/localeStore.js";
    import {vendorListStore} from "$lib/stores/foodVendorStore.js";

    $: vendorName =
        $vendorListStore.find(v => v.type === $mealPlanStore.foodVendor)
            ?.name ?? 'Forktimize';


</script>

<div class="card">
    <SectionHeader title={$t.mealPlan.yourMealPlan()}
                   subTitle={`🛵 ${$t.mealPlan.orderTheseFoods()} ${vendorName}`}>
            <span slot="tags" class="tag is-light is-success bigger-tag">
      <img src="meal-plan.png" alt="Protein" width="30" height="30"
           class="mr-2"/> {$mealPlanStore.foods.length} {$t.mealPlan.items()}
    </span>
    </SectionHeader>
    <div class="is-flex is-flex-wrap-wrap mt-5 p-3">
        {#each $mealPlanStore.foods as food}
            <FoodCard food={food}/>
        {/each}
    </div>
</div>
