<script>
    import {localeStore, t} from "$lib/stores/localeStore.js";

    export let dates;
    export let selectedDate;
    export let isValid = true;

    $: isLoading = !dates || dates.length === 0;
    $: isValid = !selectedDate || dates.includes(selectedDate);

    function formatDateLabel(date) {
        return `${date} | ${new Date(date).toLocaleDateString($localeStore, {weekday: "long"})}`;
    }

</script>

<div class="field">
    <label for="date-selector" class="label">{$t.requestForm.selectDate()} 📅 </label>
    <div class="control">
        <div class="select is-fullwidth" class:is-loading={isLoading} class:is-danger={!isValid}>
            <select id="date-selector" bind:value={selectedDate}>
                {#each dates as date}
                    <option value={date}>{formatDateLabel(date)}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
