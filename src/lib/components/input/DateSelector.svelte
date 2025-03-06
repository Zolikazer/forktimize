<script>
    export let dates = [];

    let selectedDate = dates[0]; // Default selected date
</script>

<div class="field">
    <label class="label">Select a Date 📅 </label>
    <div class="control">
        <div class="select is-fullwidth">
            <select bind:value={selectedDate}>
                {#each dates as date}
                    <option value={date}>{date}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
