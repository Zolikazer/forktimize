<script>
    import Food from "$lib/components/menu/Food.svelte";
    import { menuStore } from "$lib/stores/menuStore.js";

</script>

<div class="box">
    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Menu For Wednesday</h2>

    <div class="is-flex is-flex-wrap-wrap">
        {#each $menuStore.foods as food}
            <Food food={food}/>
        {/each}
    </div>
</div>
