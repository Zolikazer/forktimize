<script>
    import Input from "$lib/components/input/Input.svelte";
    import Help from "$lib/components/help/Help.svelte";
    import Menu from "$lib/components/menu/Menu.svelte";
    import {menuStore} from "$lib/stores/menuStore.js";
    import MenuSummary from "$lib/components/menu/MenuSummary.svelte";
    import FoodLogEntry from "$lib/components/menu/FoodLogEntry.svelte";

    export let data = {dates: []};

</script>

<section class="mt-5">
    <div class="container is-fluid">
        <div class="columns is-centered">
            <div class="column">
                <Input dates={data.dates}/>
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
