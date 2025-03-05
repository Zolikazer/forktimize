<script>
    import Input from "$lib/components/app/Input.svelte";
    import Help from "$lib/components/app/Help.svelte";
    import Menu from "$lib/components/app/Menu.svelte";
    import {menu} from "$lib/stores/menuStore.js";

</script>

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


<section class="main-container">
    <div class="container is-fluid">
        <div class="columns is-centered">
            <div class="column">
                <Input/>
            </div>
            <div class="column">
                <Help/>
            </div>
        </div>

        {#if $menu}
            <div class="columns is-centered">
                <div class="column">
                    <Menu/>
                </div>
                <div class="column">
                </div>
            </div>
        {/if}
    </div>
</section>



