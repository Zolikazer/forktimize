<script>
    import Instructions from "$lib/components/help/Instructions.svelte";
    import {menu} from "$lib/stores/menuStore.js";
</script>

<div class="box">
    {#if $menu}
        <div class="notification is-success has-text-centered">
            <strong>Your menu is ready. ✅</strong>
        </div>
    {:else}
        <div class="notification is-info has-text-centered">
            No menu generated yet. Click <strong>"Generate My Menu"</strong> to get started! 🚀
        </div>
    {/if}
    <Instructions/>
</div>
