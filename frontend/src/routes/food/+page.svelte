<script>
    import Input from "$lib/components/input/Input.svelte";
    import Help from "$lib/components/help/Help.svelte";
    import Menu from "$lib/components/menu/Menu.svelte";
    import {menu} from "$lib/stores/menuStore.js";
    import MenuSummary from "$lib/components/menu/MenuSummary.svelte";
    import Myfitnesspal from "$lib/components/myfitnesspal/Myfitnesspal.svelte";

    export let data;

</script>

<section class="main-container">
    <div class="container is-fluid">
        <div class="columns is-centered">
            <div class="column">
                <Input dates={data.dates}/>
            </div>
            <div class="column">
                <Help/>
            </div>
        </div>

        {#if $menu && $menu.length > 0}
            <div class="columns is-centered">
                <div class="column">
                    <Menu/>
                </div>
                <div class="column">
                    <MenuSummary/>
                    <Myfitnesspal/>
                </div>
            </div>
        {/if}
    </div>
</section>

<style>
    /* Main container for two-column layout */
    .main-container {
        display: flex;
        /*justify-content: center;*/
        /*gap: 2rem;*/
        /*max-width: 1200px;*/
        margin: 2rem auto;
    }

</style>

