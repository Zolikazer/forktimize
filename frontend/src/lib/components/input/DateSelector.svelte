<script>
    export let dates;

    export let selectedDate;
</script>

<div class="field">
    <label class="label">Select a Date 📅 </label>
    <div class="control">
        <div class="select is-fullwidth">
            <select bind:value={selectedDate}>
                {#each dates as date}
                    <option value={date}>{`${date} | ${new Date(date).toLocaleDateString("en-US", { weekday: "long" })}`}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
