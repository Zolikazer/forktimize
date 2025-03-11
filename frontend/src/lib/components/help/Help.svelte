<script>
    import Instructions from "$lib/components/help/Instructions.svelte";
    import {menu} from "$lib/stores/menuStore.js";
    const MenuStatus = {
        NOT_GENERATED: "notGenerated",
        SUCCESS: "success",
        FAILURE: "failure"
    };

    $: menuStatus = $menu === null
        ? MenuStatus.NOT_GENERATED
        : $menu.length > 0
            ? MenuStatus.SUCCESS
            : MenuStatus.FAILURE;
</script>

<div class="box">
    {#if menuStatus === MenuStatus.SUCCESS}
        <div class="notification is-success has-text-centered">
            <strong>Your menu is ready. ✅</strong>
        </div>
    {:else if menuStatus === MenuStatus.FAILURE}
        <div class="notification is-danger has-text-centered">
            Sorry, we could not find a menu that meets your needs. 😔 <strong>Adjust your input and try again!</strong> 👍
        </div>

    {:else}
        <div class="notification is-info has-text-centered">
            No menu generated yet. Click <strong>"Generate My Menu"</strong> to get started! 🚀
        </div>
    {/if}
    <Instructions/>
</div>
