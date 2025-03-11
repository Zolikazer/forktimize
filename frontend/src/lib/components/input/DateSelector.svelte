<script>
    export let dates = [];
    export let selectedDate = dates.length ? dates[0] : "";

    function formatDateLabel(date) {
        return `${date} | ${new Date(date).toLocaleDateString("en-US", { weekday: "long" })}`;
    }
</script>

<div class="field">
    <label for="date-selector" class="label">Select a Date 📅 </label>
    <div class="control">
        <div class="select is-fullwidth">
            <select id="date-selector" bind:value={selectedDate}>
                {#each dates as date}
                    <option value={date}>{formatDateLabel(date)}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
