<script>
    export let label;
    export let minValue;
    export let maxValue;
    export let unit = "";
</script>

<div class="input-group has-background-white-ter">
    <p class="has-text-weight-bold has-text-grey-darker is-size-7 mb-2">{label} ({unit})</p>

    <div class="is-flex is-justify-content-center gap-2">
        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Min</label>
            <input type="number" bind:value={minValue} class="input is-small has-text-centered is-rounded" placeholder="Min">
        </div>
        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Max</label>
            <input type="number" bind:value={maxValue} class="input is-small has-text-centered is-rounded" placeholder="Max">
        </div>
    </div>
</div>


<style>
    .input-group {
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.45);
        text-align: center;
        font-size: 0.9rem;
        width: 200px; /* Adjusted width to fit inline */
        margin: auto;
    }
</style>
