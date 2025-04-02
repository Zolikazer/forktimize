<script>
    import FoodCard from "$lib/components/menu/meal-plan/FoodCard.svelte";
    import {menuStore} from "$lib/stores/menuStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import {getProviderLabel} from "$lib/utils/foodProviders.js";
</script>

<div class="card">
    <!--    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Menu For Wednesday</h2>-->
    <SectionHeader title="Your Food Plan" subTitle={`🛵 Order these from ${getProviderLabel($menuStore.foodProvider)}`}>
            <span slot="tags" class="tag is-light is-success bigger-tag">
      🍱 {$menuStore.foods.length} items
    </span>
    </SectionHeader>
    <div class="is-flex is-flex-wrap-wrap mt-5 p-3">
        {#each $menuStore.foods as food}
            <FoodCard food={food}/>
        {/each}
    </div>
</div>
