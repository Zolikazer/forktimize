<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import {fade} from 'svelte/transition';
    import MenuRequestForm from "$lib/components/forms/MenuRequestForm.svelte";
    import Help from "$lib/components/feedback/Help.svelte";
    import Menu from "$lib/components/menu/food-plan/Menu.svelte";
    import MenuSummary from "$lib/components/menu/insights/summary/MenuSummary.svelte";
    import FoodLogEntry from "$lib/components/menu/insights/food-log/FoodLogEntry.svelte";

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
            <div class="columns is-centered" transition:fade={{ duration: 150 }}>
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
