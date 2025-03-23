<script>
    import {onMount} from "svelte";
    import {getDates} from "$lib/api/foodPlannerClient.js";
    import {menuFormStore} from "$lib/stores/menuFormStore.js";

    let dates = getDefaultAvailableDates();
    menuFormStore.setSelectedDate(dates[0])

    onMount(async () => {
        try {
            dates = await getDates();
            menuFormStore.setSelectedDate(dates[0])
        } catch (err) {
        }
    });

    function getDefaultAvailableDates() {
        const generatedDates = [];
        let date = new Date();
        date.setDate(date.getDate() + 1);

        while (generatedDates.length < 10) {
            date.setDate(date.getDate() + 1);
            if (date.getDay() !== 0) {
                generatedDates.push(date.toISOString().split("T")[0]);
            }
        }
        return generatedDates;
    }

    function formatDateLabel(date) {
        return `${date} | ${new Date(date).toLocaleDateString("en-US", {weekday: "long"})}`;
    }
</script>

<div class="field">
    <label for="date-selector" class="label">Select a Date 📅 </label>
    <div class="control">
        <div class="select is-fullwidth">
            <select id="date-selector" bind:value={$menuFormStore.selectedDate}>
                {#each dates as date}
                    <option value={date}>{formatDateLabel(date)}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
