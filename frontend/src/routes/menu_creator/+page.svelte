<script>
    import MenuRequestForm from "$lib/components/forms/MenuRequestForm.svelte";
    import Help from "$lib/components/help/Help.svelte";
    import Menu from "$lib/components/menu/food-plan/Menu.svelte";
    import {menuStore} from "$lib/stores/menuStore.js";
    import FoodLogEntry from "$lib/components/menu/food-log/FoodLogEntry.svelte";
    import MenuSummary from "$lib/components/menu/summary/MenuSummary.svelte";

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

        {#if $menuStore.foods && $menuStore.foods.length > 0}
            <div class="columns is-centered">
                <div class="column">
                    <Menu/>
                </div>
                <div class="column">
                    <MenuSummary/>
                    <FoodLogEntry/>
                </div>
            </div>
        {/if}
    </div>
</section>
