<script>
    import {onMount} from "svelte";
    import {getDates} from "$lib/api/foodPlannerApi.js";
    import {menuRequestStore} from "$lib/stores/menuRequestStore.js";

    let dates = getDefaultAvailableDates();
    onMount(async () => {
        try {
            dates = await getDates();
            menuRequestStore.setSelectedDate(dates[0])

        } catch (err) {
        }
    });

    function getDefaultAvailableDates() {
        const generatedDates = [];
        let currentDate = new Date();

        while (generatedDates.length < 10) {
            currentDate.setDate(currentDate.getDate() + 1);

            if (currentDate.getDay() !== 0) {
                generatedDates.push(currentDate.toISOString().split("T")[0]);
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
            <select id="date-selector" bind:value={$menuRequestStore.selectedDate}>
                {#each dates as date}
                    <option value={date}>{formatDateLabel(date)}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
