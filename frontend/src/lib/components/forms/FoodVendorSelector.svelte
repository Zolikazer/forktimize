<script>
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
    import {t} from "$lib/stores/localeStore.js";
    import {vendorListStore} from "$lib/stores/foodVendorStore.js";

    $: isVendorLoading = $vendorListStore.length === 0;

    function handleVendorChange(event) {
        const newVendor = event.target.value;
        mealPlanRequestStore.setVendor(newVendor);
        console.log($mealPlanRequestStore);
    }

</script>

<div class="field tag is-light is-success bigger-tag is-flex is-justify-content-space-between is-align-items-center">
    <span>🧑‍🍳 {$t.requestForm.kitchen()}:</span>

    <div class="control is-light ml-1">
        <div class="select is-primary is-small styled-select" class:is-loading={isVendorLoading}>
            <select class="has-text-weight-bold is-loading"
                    on:change={handleVendorChange}>
                {#each $vendorListStore as vendor}
                    <option value={vendor.type}>{vendor.name}</option>
                {/each}
            </select>
        </div>
    </div>
</div>

<style>

    .styled-select select {
        background-color: #f5f5f5;
        border: none;
        color: #363636;

        font-size: 1.1rem;
        line-height: 1;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        height: 1.8em;
    }

    .styled-select select:hover {
        background-color: #eeeeee;
    }

    .styled-select select:focus {
        box-shadow: 0 0 0 0.125em rgba(0, 209, 178, 0.25);
    }


</style>
