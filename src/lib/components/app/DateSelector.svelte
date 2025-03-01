<script>
    let today = new Date();
    let dates = [];

    // Generate the next 10 dates dynamically
    for (let i = 0; i < 10; i++) {
        let futureDate = new Date();
        futureDate.setDate(today.getDate() + i);
        dates.push(futureDate.toISOString().split("T")[0]); // Format: YYYY-MM-DD
    }

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
