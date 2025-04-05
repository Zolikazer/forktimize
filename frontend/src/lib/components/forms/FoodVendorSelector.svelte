<script>
    import {foodVendorList} from "$lib/utils/foodVendors.js";
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
</script>

<div class="field tag is-light is-success bigger-tag is-flex is-justify-content-space-between is-align-items-center">
    <span>🧑‍🍳 Kitchen:</span>

    <div class="control is-light ml-1">
        <div class="select is-primary is-small styled-select">
            <select class="has-text-weight-bold" bind:value={$mealPlanRequestStore.foodVendor}>
                {#each foodVendorList as { label, value }}
                    <option value={value}>{label}</option>
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
