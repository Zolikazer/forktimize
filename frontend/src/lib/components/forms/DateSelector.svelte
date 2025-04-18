<script>
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
    import {localeStore, t} from "$lib/stores/localeStore.js";
    import {vendorListStore} from "$lib/stores/foodVendorStore.js";

    function formatDateLabel(date) {
        return `${date} | ${new Date(date).toLocaleDateString($localeStore, {weekday: "long"})}`;
    }

    $: dates =
        $vendorListStore.find(v => v.type === $mealPlanRequestStore.foodVendor)
            ?.availableDates ?? [];

    let hasSetInitialDate = false;

    $: if (
        dates.length > 0 &&
        !$mealPlanRequestStore.selectedDate &&
        !hasSetInitialDate
    ) {
        hasSetInitialDate = true;
        mealPlanRequestStore.setSelectedDate(dates[0]);
    }

</script>

<div class="field">
    <label for="date-selector" class="label">{$t.requestForm.selectDate()} 📅 </label>
    <div class="control">
        <div class="select is-fullwidth" class:is-loading={!hasSetInitialDate}>
            <select id="date-selector" bind:value={$mealPlanRequestStore.selectedDate}>
                {#each dates as date}
                    <option value={date}>{formatDateLabel(date)}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
