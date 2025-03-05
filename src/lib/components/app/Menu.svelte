<script>
    import Food from "$lib/components/app/Food.svelte";
    import { menu } from "$lib/stores/menuStore.js";

</script>

<div class="box">
    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Menu On Wednesday</h2>

    <div class="is-flex is-flex-wrap-wrap is-justify-content-center">
        {#each $menu as food}
            <Food food={food}/>
        {/each}
    </div>
</div>
